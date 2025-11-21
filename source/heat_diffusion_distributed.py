"""
Difusão de Calor 2D - Versão Distribuída com Sockets
Arquitetura Master-Worker usando TCP sockets

Master: coordena workers, distribui linhas da malha, agrega resultados
Workers: processam subconjuntos de linhas, comunicam via sockets
"""

import numpy as np
import socket
import pickle
import time
import json
import threading
from typing import Tuple, Dict, List


class HeatDiffusionMaster:
    """
    Nó Master: coordena workers distribuídos.
    """
    
    def __init__(self, grid_size: int, alpha: float, max_iterations: int,
                 tolerance: float, worker_hosts: List[Tuple[str, int]]):
        self.N = grid_size
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.worker_hosts = worker_hosts
        self.num_workers = len(worker_hosts)
        
        # Discretização
        self.dx = 1.0 / (self.N - 1)
        self.dy = 1.0 / (self.N - 1)
        self.dt = (self.dx ** 2 * self.dy ** 2) / (2 * self.alpha * (self.dx ** 2 + self.dy ** 2))
        
        # Matriz de temperatura
        self.u_old = np.zeros((self.N, self.N), dtype=np.float64)
        self.u_new = np.zeros((self.N, self.N), dtype=np.float64)
        
        self._initialize_conditions()
        self._setup_worker_ranges()
    
    def _initialize_conditions(self):
        """Condições iniciais."""
        self.u_old[:, 0] = 0.0
        self.u_old[:, -1] = 0.0
        self.u_old[0, :] = 0.0
        self.u_old[-1, :] = 100.0
        self.u_old[1:-1, 1:-1] = 25.0
        
        center = self.N // 2
        self.u_old[center-2:center+2, center-2:center+2] = 80.0
    
    def _setup_worker_ranges(self):
        """Divide linhas entre workers."""
        rows_per_worker = (self.N - 2) // self.num_workers
        self.worker_ranges = []
        
        for w in range(self.num_workers):
            start_row = 1 + w * rows_per_worker
            
            if w == self.num_workers - 1:
                end_row = self.N - 1
            else:
                end_row = start_row + rows_per_worker
            
            self.worker_ranges.append((start_row, end_row))
    
    def _send_data(self, sock: socket.socket, data: dict):
        """Envia dados serializados via socket."""
        serialized = pickle.dumps(data)
        size = len(serialized)
        
        # Envia tamanho primeiro (4 bytes)
        sock.sendall(size.to_bytes(4, byteorder='big'))
        # Envia dados
        sock.sendall(serialized)
    
    def _receive_data(self, sock: socket.socket) -> dict:
        """Recebe dados serializados via socket."""
        # Recebe tamanho (4 bytes)
        size_bytes = sock.recv(4)
        size = int.from_bytes(size_bytes, byteorder='big')
        
        # Recebe dados
        data = b''
        while len(data) < size:
            packet = sock.recv(min(size - len(data), 4096))
            if not packet:
                break
            data += packet
        
        return pickle.loads(data)
    
    def solve(self) -> Tuple[int, float, float]:
        """Executa simulação distribuída."""
        start_time = time.time()
        
        # Conecta aos workers
        worker_sockets = []
        for host, port in self.worker_hosts:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            worker_sockets.append(sock)
            print(f"Conectado ao worker {host}:{port}")
        
        # Envia configuração inicial para workers
        for i, sock in enumerate(worker_sockets):
            start_row, end_row = self.worker_ranges[i]
            config = {
                'type': 'config',
                'worker_id': i,
                'N': self.N,
                'alpha': self.alpha,
                'dx': self.dx,
                'dy': self.dy,
                'dt': self.dt,
                'start_row': start_row,
                'end_row': end_row
            }
            self._send_data(sock, config)
        
        # Loop de iterações
        for iteration in range(self.max_iterations):
            global_max_diff = 0.0
            
            # Envia dados para workers
            for i, sock in enumerate(worker_sockets):
                start_row, end_row = self.worker_ranges[i]
                
                # Inclui linhas fantasma (ghost rows) para vizinhos
                start_with_ghost = max(0, start_row - 1)
                end_with_ghost = min(self.N, end_row + 1)
                
                work_data = {
                    'type': 'work',
                    'iteration': iteration,
                    'u_data': self.u_old[start_with_ghost:end_with_ghost, :].copy()
                }
                self._send_data(sock, work_data)
            
            # Recebe resultados dos workers
            for i, sock in enumerate(worker_sockets):
                result = self._receive_data(sock)
                
                start_row, end_row = self.worker_ranges[i]
                
                # Atualiza matriz com resultados
                self.u_new[start_row:end_row, :] = result['u_computed']
                
                # Atualiza erro máximo
                if result['max_diff'] > global_max_diff:
                    global_max_diff = result['max_diff']
            
            # Mantém condições de contorno
            self.u_new[:, 0] = self.u_old[:, 0]
            self.u_new[:, -1] = self.u_old[:, -1]
            self.u_new[0, :] = self.u_old[0, :]
            self.u_new[-1, :] = self.u_old[-1, :]
            
            # Troca buffers
            self.u_old, self.u_new = self.u_new, self.u_old
            
            # Verifica convergência
            if global_max_diff < self.tolerance:
                # Envia sinal de parada
                for sock in worker_sockets:
                    stop_signal = {'type': 'stop'}
                    self._send_data(sock, stop_signal)
                
                # Fecha conexões
                for sock in worker_sockets:
                    sock.close()
                
                end_time = time.time()
                return iteration + 1, end_time - start_time, global_max_diff
        
        # Máximo de iterações atingido
        for sock in worker_sockets:
            stop_signal = {'type': 'stop'}
            self._send_data(sock, stop_signal)
            sock.close()
        
        end_time = time.time()
        return self.max_iterations, end_time - start_time, global_max_diff
    
    def get_temperature_field(self) -> np.ndarray:
        """Retorna campo de temperatura."""
        return self.u_old.copy()


class HeatDiffusionWorker:
    """
    Nó Worker: processa parte da malha.
    """
    
    def __init__(self, port: int):
        self.port = port
        self.config = None
        self.u_local = None
    
    def _send_data(self, sock: socket.socket, data: dict):
        """Envia dados."""
        serialized = pickle.dumps(data)
        size = len(serialized)
        sock.sendall(size.to_bytes(4, byteorder='big'))
        sock.sendall(serialized)
    
    def _receive_data(self, sock: socket.socket) -> dict:
        """Recebe dados."""
        size_bytes = sock.recv(4)
        if not size_bytes:
            return None
        size = int.from_bytes(size_bytes, byteorder='big')
        
        data = b''
        while len(data) < size:
            packet = sock.recv(min(size - len(data), 4096))
            if not packet:
                break
            data += packet
        
        return pickle.loads(data)
    
    def _compute_work(self, u_data: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Processa linhas atribuídas.
        u_data inclui linhas fantasma.
        """
        # Dimensões locais
        local_rows = self.config['end_row'] - self.config['start_row']
        N = self.config['N']
        
        u_result = np.zeros((local_rows, N), dtype=np.float64)
        max_diff = 0.0
        
        dx = self.config['dx']
        dy = self.config['dy']
        dt = self.config['dt']
        alpha = self.config['alpha']
        
        # Índices ajustados para linhas fantasma
        for local_i in range(local_rows):
            i = local_i + 1  # Offset para linha fantasma superior
            
            for j in range(1, N - 1):
                d2u_dx2 = (u_data[i+1, j] - 2*u_data[i, j] + u_data[i-1, j]) / (dx ** 2)
                d2u_dy2 = (u_data[i, j+1] - 2*u_data[i, j] + u_data[i, j-1]) / (dy ** 2)
                
                u_result[local_i, j] = u_data[i, j] + alpha * dt * (d2u_dx2 + d2u_dy2)
                
                diff = abs(u_result[local_i, j] - u_data[i, j])
                if diff > max_diff:
                    max_diff = diff
        
        return u_result, max_diff
    
    def start(self):
        """Inicia worker e aguarda múltiplas conexões do master."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(5)  # Permite fila de conexões
    
        print(f"Worker aguardando conexões na porta {self.port}...")
    
        # Loop para aceitar múltiplas conexões
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Nova conexão do master {addr}")
            
                # Recebe configuração
                self.config = self._receive_data(client_socket)
            
                if self.config is None:
                    break
                
                print(f"Worker {self.config['worker_id']} configurado: linhas {self.config['start_row']}-{self.config['end_row']}")
            
                # Loop de trabalho para esta conexão
                while True:
                    data = self._receive_data(client_socket)
                
                    if data is None or data['type'] == 'stop':
                        print("Worker finalizou benchmark")
                        break
                
                    if data['type'] == 'work':
                        u_data = data['u_data']
                        u_computed, max_diff = self._compute_work(u_data)
                    
                        result = {
                            'u_computed': u_computed,
                            'max_diff': max_diff
                        }
                        self._send_data(client_socket, result)
            
                client_socket.close()
                print("Conexão fechada. Aguardando próximo benchmark...\n")
            
            except KeyboardInterrupt:
                print("\nWorker sendo encerrado...")
                break
            except Exception as e:
                print(f"Erro no worker: {e}")
                continue
    
        server_socket.close()
        print("Worker encerrado completamente")


def benchmark_distributed(grid_sizes: list = [50, 100, 200],
                         worker_counts: list = [1, 2, 4],
                         repetitions: int = 3) -> Dict:
    """
    Benchmark versão distribuída.
    NOTA: Requer workers rodando em máquinas/portas separadas.
    """
    results = {
        'grid_sizes': grid_sizes,
        'worker_counts': worker_counts,
        'times': {},
        'speedups': {}
    }
    
    print("=" * 60)
    print("BENCHMARK - VERSÃO DISTRIBUÍDA (SOCKETS)")
    print("=" * 60)
    print("NOTA: Este benchmark requer workers rodando previamente")
    print("Inicie workers com: python heat_diffusion_distributed.py --worker --port <PORT>")
    print("=" * 60)
    
    for grid_size in grid_sizes:
        results['times'][grid_size] = {}
        results['speedups'][grid_size] = {}
        
        baseline_time = None
        
        for num_workers in worker_counts:
            # Define hosts dos workers (localhost para teste)
            worker_hosts = [('localhost', 5000 + i) for i in range(num_workers)]
            
            times_run = []
            
            for rep in range(repetitions):
                print(f"\nMalha {grid_size}x{grid_size} - {num_workers} workers - Rep {rep+1}/{repetitions}")
                
                try:
                    master = HeatDiffusionMaster(
                        grid_size=grid_size,
                        alpha=0.01,
                        max_iterations=10000,
                        tolerance=1e-4,
                        worker_hosts=worker_hosts
                    )
                    
                    iters, exec_time, error = master.solve()
                    times_run.append(exec_time)
                    
                    print(f"  Tempo: {exec_time:.4f}s")
                except Exception as e:
                    print(f"  ERRO: {e}")
                    continue
            
            if times_run:
                avg_time = np.mean(times_run)
                results['times'][grid_size][num_workers] = avg_time
                
                if num_workers == 1:
                    baseline_time = avg_time
                    results['speedups'][grid_size][num_workers] = 1.0
                elif baseline_time:
                    speedup = baseline_time / avg_time
                    results['speedups'][grid_size][num_workers] = speedup
                
                print(f">>> Média {num_workers} workers: {avg_time:.4f}s", end="")
                if num_workers > 1 and baseline_time:
                    print(f" (Speedup: {results['speedups'][grid_size][num_workers]:.2f}x)")
                else:
                    print()
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Heat Diffusion - Distributed Version')
    parser.add_argument('--worker', action='store_true', help='Run as worker')
    parser.add_argument('--port', type=int, default=5000, help='Worker port')
    parser.add_argument('--benchmark', action='store_true', help='Run benchmark as master')
    
    args = parser.parse_args()
    
    if args.worker:
        # Modo worker
        worker = HeatDiffusionWorker(port=args.port)
        worker.start()
    elif args.benchmark:
        # Modo benchmark
        results = benchmark_distributed(
            grid_sizes=[50, 100, 200],
            worker_counts=[1, 2, 4],
            repetitions=3
        )
        
        with open('distributed_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\n" + "=" * 60)
        print("Resultados salvos em 'distributed_results.json'")
        print("=" * 60)
    else:
        print("Use --worker para iniciar worker ou --benchmark para executar benchmark")
