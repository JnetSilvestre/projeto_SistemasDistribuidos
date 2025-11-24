"""
Difusão de Calor 2D - Versão Paralela com Threads
Paralelização por divisão de linhas da malha

"""

import numpy as np
import time
import json
import threading
from typing import Tuple, Dict, List


class HeatDiffusion2DParallel:
    """
    Simula difusão de calor em 2D usando threads para paralelização.
    A malha é dividida horizontalmente entre threads.
    
    """
    
    def __init__(self, grid_size: int = 100, alpha: float = 0.01,
                 max_iterations: int = 10000, tolerance: float = 1e-4,
                 num_threads: int = 4):
        self.N = grid_size
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.num_threads = num_threads
        
        # Parâmetros de discretização
        self.dx = 1.0 / (self.N - 1)
        self.dy = 1.0 / (self.N - 1)
        self.dt = (self.dx ** 2 * self.dy ** 2) / (2 * self.alpha * (self.dx ** 2 + self.dy ** 2))
        
        # Matrizes de temperatura
        self.u_old = np.zeros((self.N, self.N), dtype=np.float64)
        self.u_new = np.zeros((self.N, self.N), dtype=np.float64)
        
        # Sincronização entre threads
        self.barrier = threading.Barrier(self.num_threads)
        self.lock = threading.Lock()
        self.global_max_diff = 0.0
        
        self._initialize_conditions()
        self._setup_thread_ranges()
    
    def _initialize_conditions(self):
        """Define condições iniciais e de contorno."""
        self.u_old[:, 0] = 0.0
        self.u_old[:, -1] = 0.0
        self.u_old[0, :] = 0.0
        self.u_old[-1, :] = 100.0
        self.u_old[1:-1, 1:-1] = 25.0
        
        center = self.N // 2
        self.u_old[center-2:center+2, center-2:center+2] = 80.0
    
    def _setup_thread_ranges(self):
        """Divide a malha entre threads."""
        rows_per_thread = (self.N - 2) // self.num_threads
        self.thread_ranges = []
        
        for t in range(self.num_threads):
            start_row = 1 + t * rows_per_thread
            
            if t == self.num_threads - 1:
                end_row = self.N - 1  # Última thread pega linhas restantes
            else:
                end_row = start_row + rows_per_thread
            
            self.thread_ranges.append((start_row, end_row))
    
    def _compute_thread_work(self, start_row: int, end_row: int) -> float:
        """
        Trabalho executado por uma thread: atualiza linhas [start_row, end_row).
        """
        local_max_diff = 0.0
        
        for i in range(start_row, end_row):
            for j in range(1, self.N - 1):
                d2u_dx2 = (self.u_old[i+1, j] - 2*self.u_old[i, j] + self.u_old[i-1, j]) / (self.dx ** 2)
                d2u_dy2 = (self.u_old[i, j+1] - 2*self.u_old[i, j] + self.u_old[i, j-1]) / (self.dy ** 2)
                
                self.u_new[i, j] = self.u_old[i, j] + self.alpha * self.dt * (d2u_dx2 + d2u_dy2)
                
                diff = abs(self.u_new[i, j] - self.u_old[i, j])
                if diff > local_max_diff:
                    local_max_diff = diff
        
        return local_max_diff
    
    def _thread_worker(self, thread_id: int, iteration_count: List[int]):
        """Função executada por cada thread."""
        start_row, end_row = self.thread_ranges[thread_id]
        
        for iteration in range(self.max_iterations):
            # Computa trabalho local
            local_max_diff = self._compute_thread_work(start_row, end_row)
            
            # Atualiza erro global (região crítica)
            with self.lock:
                if local_max_diff > self.global_max_diff:
                    self.global_max_diff = local_max_diff
            
            # Sincroniza threads antes de trocar buffers
            self.barrier.wait()
            
            # Apenas a thread 0 faz verificação de convergência
            if thread_id == 0:
                converged = self.global_max_diff < self.tolerance
                
                # Troca buffers
                self.u_old, self.u_new = self.u_new, self.u_old
                
                # Reseta erro global para próxima iteração
                self.global_max_diff = 0.0
                
                iteration_count[0] = iteration + 1
                
                if converged:
                    # Sinaliza parada para outras threads
                    self.stop_flag = True
            
            # Sincroniza novamente antes de próxima iteração
            self.barrier.wait()
            
            # Verifica flag de parada
            if hasattr(self, 'stop_flag') and self.stop_flag:
                break
    
    def solve(self) -> Tuple[int, float, float]:
        """Executa simulação paralela."""
        self.stop_flag = False
        iteration_count = [0]
        
        start_time = time.time()
        
        # Cria e inicia threads
        threads = []
        for t in range(self.num_threads):
            thread = threading.Thread(
                target=self._thread_worker,
                args=(t, iteration_count)
            )
            threads.append(thread)
            thread.start()
        
        # Aguarda conclusão
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        return iteration_count[0], end_time - start_time, self.global_max_diff
    
    def get_temperature_field(self) -> np.ndarray:
        """Retorna campo de temperatura."""
        return self.u_old.copy()


def benchmark_parallel(grid_sizes: list = [50, 100, 200, 400],
                      thread_counts: list = [1, 2, 4, 8],
                      repetitions: int = 3) -> Dict:
    """Benchmark versão paralela variando malha e número de threads."""
    results = {
        'grid_sizes': grid_sizes,
        'thread_counts': thread_counts,
        'times': {},  # times[grid_size][num_threads]
        'speedups': {}
    }
    
    print("=" * 60)
    print("BENCHMARK - VERSÃO PARALELA (THREADS)")
    print("=" * 60)
    
    for grid_size in grid_sizes:
        results['times'][grid_size] = {}
        results['speedups'][grid_size] = {}
        
        baseline_time = None
        
        for num_threads in thread_counts:
            times_run = []
            
            for rep in range(repetitions):
                print(f"\nMalha {grid_size}x{grid_size} - {num_threads} threads - Rep {rep+1}/{repetitions}")
                
                solver = HeatDiffusion2DParallel(
                    grid_size=grid_size,
                    alpha=0.01,
                    max_iterations=10000,
                    tolerance=1e-4,
                    num_threads=num_threads
                )
                
                iters, exec_time, error = solver.solve()
                times_run.append(exec_time)
                
                print(f"  Tempo: {exec_time:.4f}s")
            
            avg_time = np.mean(times_run)
            results['times'][grid_size][num_threads] = avg_time
            
            # Calcula speedup relativo a 1 thread
            if num_threads == 1:
                baseline_time = avg_time
                results['speedups'][grid_size][num_threads] = 1.0
            else:
                speedup = baseline_time / avg_time
                results['speedups'][grid_size][num_threads] = speedup
            
            print(f">>> Média {num_threads} threads: {avg_time:.4f}s", end="")
            if num_threads > 1:
                print(f" (Speedup: {results['speedups'][grid_size][num_threads]:.2f}x)")
            else:
                print()
    
    return results


if __name__ == "__main__":
    results = benchmark_parallel(
        grid_sizes=[50, 100, 200, 300],
        thread_counts=[1, 2, 4, 8],
        repetitions=3
    )
    
    with open('parallel_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Resultados salvos em 'parallel_results.json'")
    print("=" * 60)
