"""
Difusão de Calor 2D - Versão Sequencial
Implementação usando método de diferenças finitas (FTCS)

"""

import numpy as np
import time
import json
from typing import Tuple, Dict
import matplotlib.pyplot as plt


class HeatDiffusion2DSequential:
    
    def __init__(self, grid_size: int = 100, alpha: float = 0.01, 
                 max_iterations: int = 10000, tolerance: float = 1e-4):
        self.N = grid_size
        self.alpha = alpha
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        
        # Parâmetros de discretização
        self.dx = 1.0 / (self.N - 1)
        self.dy = 1.0 / (self.N - 1)
        
        # Critério de estabilidade CFL (Courant-Friedrichs-Lewy)
        self.dt = (self.dx ** 2 * self.dy ** 2) / (2 * self.alpha * (self.dx ** 2 + self.dy ** 2))
        
        # Matrizes de temperatura
        self.u_old = np.zeros((self.N, self.N), dtype=np.float64)
        self.u_new = np.zeros((self.N, self.N), dtype=np.float64)
        
        self._initialize_conditions()
    
    def _initialize_conditions(self):
        """Define condições iniciais e de contorno."""
        # Condições de contorno (bordas)
        self.u_old[:, 0] = 0.0    # Esquerda
        self.u_old[:, -1] = 0.0   # Direita
        self.u_old[0, :] = 0.0    # Topo
        self.u_old[-1, :] = 100.0 # Base (fonte de calor)
        
        # Condição inicial: temperatura uniforme no interior
        self.u_old[1:-1, 1:-1] = 25.0
        
        # Fonte de calor pontual no centro
        center = self.N // 2
        self.u_old[center-2:center+2, center-2:center+2] = 80.0
    
    def _compute_iteration(self) -> float:
        """
        Executa uma iteração do método de diferenças finitas.
        Retorna o erro máximo (critério de convergência).
        """
        max_diff = 0.0
        
        # Atualiza pontos internos da malha
        for i in range(1, self.N - 1):
            for j in range(1, self.N - 1):
                # Diferenças finitas centrais
                d2u_dx2 = (self.u_old[i+1, j] - 2*self.u_old[i, j] + self.u_old[i-1, j]) / (self.dx ** 2)
                d2u_dy2 = (self.u_old[i, j+1] - 2*self.u_old[i, j] + self.u_old[i, j-1]) / (self.dy ** 2)
                
                # Atualização temporal
                self.u_new[i, j] = self.u_old[i, j] + self.alpha * self.dt * (d2u_dx2 + d2u_dy2)
                
                # Calcula diferença para critério de parada
                diff = abs(self.u_new[i, j] - self.u_old[i, j])
                if diff > max_diff:
                    max_diff = diff
        
        # Mantém condições de contorno
        self.u_new[:, 0] = self.u_old[:, 0]
        self.u_new[:, -1] = self.u_old[:, -1]
        self.u_new[0, :] = self.u_old[0, :]
        self.u_new[-1, :] = self.u_old[-1, :]
        
        return max_diff
    
    def solve(self) -> Tuple[int, float, float]:
        """
        Executa a simulação até convergência ou número máximo de iterações.
        
        Retorna:
            - número de iterações
            - tempo de execução (segundos)
            - erro final
        """
        start_time = time.time()
        
        for iteration in range(self.max_iterations):
            max_diff = self._compute_iteration()
            
            # Troca buffers (evita cópia cara)
            self.u_old, self.u_new = self.u_new, self.u_old
            
            # Verifica convergência
            if max_diff < self.tolerance:
                end_time = time.time()
                return iteration + 1, end_time - start_time, max_diff
        
        end_time = time.time()
        return self.max_iterations, end_time - start_time, max_diff
    
    def get_temperature_field(self) -> np.ndarray:
        """Retorna o campo de temperatura atual."""
        return self.u_old.copy()
    
    def visualize(self, save_path: str = None):
        """Gera visualização do campo de temperatura."""
        plt.figure(figsize=(10, 8))
        plt.imshow(self.u_old, cmap='hot', interpolation='bilinear', origin='lower')
        plt.colorbar(label='Temperatura (°C)')
        plt.title(f'Difusão de Calor 2D - Malha {self.N}x{self.N}')
        plt.xlabel('X')
        plt.ylabel('Y')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()


def benchmark_sequential(grid_sizes: list = [50, 100, 200, 400], 
                        repetitions: int = 3) -> Dict:
    """
    Executa benchmark da versão sequencial para diferentes tamanhos de malha.
    """
    results = {
        'grid_sizes': grid_sizes,
        'times': [],
        'iterations': [],
        'errors': []
    }
    
    print("=" * 60)
    print("BENCHMARK - VERSÃO SEQUENCIAL")
    print("=" * 60)
    
    for grid_size in grid_sizes:
        times_run = []
        iterations_run = []
        errors_run = []
        
        for rep in range(repetitions):
            print(f"\nMalha {grid_size}x{grid_size} - Repetição {rep+1}/{repetitions}")
            
            solver = HeatDiffusion2DSequential(
                grid_size=grid_size,
                alpha=0.01,
                max_iterations=10000,
                tolerance=1e-4
            )
            
            iters, exec_time, error = solver.solve()
            
            times_run.append(exec_time)
            iterations_run.append(iters)
            errors_run.append(error)
            
            print(f"  Iterações: {iters}")
            print(f"  Tempo: {exec_time:.4f}s")
            print(f"  Erro final: {error:.2e}")
        
        # Média das repetições
        avg_time = np.mean(times_run)
        avg_iters = np.mean(iterations_run)
        avg_error = np.mean(errors_run)
        
        results['times'].append(avg_time)
        results['iterations'].append(avg_iters)
        results['errors'].append(avg_error)
        
        print(f"\n>>> MÉDIA - Malha {grid_size}x{grid_size}:")
        print(f"    Tempo: {avg_time:.4f}s (±{np.std(times_run):.4f}s)")
        print(f"    Iterações: {avg_iters:.1f}")
    
    return results


if __name__ == "__main__":
    # Benchmark com diferentes tamanhos de malha
    results = benchmark_sequential(
        grid_sizes=[50, 100, 200, 300],
        repetitions=3
    )
    
    # Salva resultados
    with open('sequential_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Resultados salvos em 'sequential_results.json'")
    print("=" * 60)
