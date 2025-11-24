"""
Script de análise comparativa dos resultados.
Gera tabelas e gráficos comparando as três implementações.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict


def load_results():
    """Carrega resultados dos arquivos JSON."""
    try:
        with open('sequential_results.json', 'r') as f:
            seq_results = json.load(f)
    except FileNotFoundError:
        seq_results = None
    
    try:
        with open('parallel_results.json', 'r') as f:
            par_results = json.load(f)
    except FileNotFoundError:
        par_results = None
    
    try:
        with open('distributed_results.json', 'r') as f:
            dist_results = json.load(f)
    except FileNotFoundError:
        dist_results = None
    
    return seq_results, par_results, dist_results


def create_comparison_table(seq_results, par_results, dist_results):
    """Cria tabela comparativa de tempos de execução."""
    print("\n" + "=" * 80)
    print("TABELA COMPARATIVA DE TEMPOS DE EXECUÇÃO")
    print("=" * 80)
    
    if not seq_results:
        print("Resultados sequenciais não encontrados!")
        return
    
    grid_sizes = seq_results['grid_sizes']
    
    # DataFrame para comparação
    data = []
    
    for i, grid_size in enumerate(grid_sizes):
        row = {
            'Tamanho da Malha': f'{grid_size}x{grid_size}',
            'Sequencial (s)': f"{seq_results['times'][i]:.4f}"
        }
        
        # Adiciona resultados paralelos
        if par_results and str(grid_size) in par_results['times']:
            for num_threads in sorted(par_results['thread_counts']):
                time_val = par_results['times'][str(grid_size)].get(str(num_threads), '-')
                speedup_val = par_results['speedups'][str(grid_size)].get(str(num_threads), '-')
                
                if time_val != '-':
                    row[f'Paralelo {num_threads}T (s)'] = f"{time_val:.4f}"
                    if speedup_val != '-':
                        row[f'Speedup {num_threads}T'] = f"{speedup_val:.2f}x"
        
        # Adiciona resultados distribuídos
        if dist_results and str(grid_size) in dist_results['times']:
            for num_workers in sorted(dist_results['worker_counts']):
                time_val = dist_results['times'][str(grid_size)].get(str(num_workers), '-')
                speedup_val = dist_results['speedups'][str(grid_size)].get(str(num_workers), '-')
                
                if time_val != '-':
                    row[f'Distribuído {num_workers}W (s)'] = f"{time_val:.4f}"
                    if speedup_val != '-':
                        row[f'Speedup {num_workers}W'] = f"{speedup_val:.2f}x"
        
        data.append(row)
    
    df = pd.DataFrame(data)
    print(df.to_string(index=False))
    print("=" * 80)
    
    # Salva como CSV
    df.to_csv('comparison_table.csv', index=False)
    print("\nTabela salva em 'comparison_table.csv'")


def plot_execution_times(seq_results, par_results, dist_results):
    """Gráfico de tempos de execução vs tamanho da malha."""
    if not seq_results:
        return
    
    grid_sizes = seq_results['grid_sizes']
    seq_times = seq_results['times']
    
    plt.figure(figsize=(12, 7))
    
    # Sequencial
    plt.plot(grid_sizes, seq_times, 'o-', linewidth=2, markersize=8, label='Sequencial')
    
    # Paralelo
    if par_results:
        for num_threads in par_results['thread_counts']:
            times = [par_results['times'][str(gs)].get(str(num_threads), None) 
                    for gs in grid_sizes]
            if None not in times:
                plt.plot(grid_sizes, times, 'o--', linewidth=2, markersize=6,
                        label=f'Paralelo ({num_threads} threads)')
    
    # Distribuído
    if dist_results:
        for num_workers in dist_results['worker_counts']:
            times = [dist_results['times'][str(gs)].get(str(num_workers), None)
                    for gs in grid_sizes]
            if None not in times:
                plt.plot(grid_sizes, times, 's-.', linewidth=2, markersize=6,
                        label=f'Distribuído ({num_workers} workers)')
    
    plt.xlabel('Tamanho da Malha (NxN)', fontsize=12, fontweight='bold')
    plt.ylabel('Tempo de Execução (segundos)', fontsize=12, fontweight='bold')
    plt.title('Comparação de Desempenho: Sequencial vs Paralelo vs Distribuído', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig('execution_times_comparison.png', dpi=300)
    print("Gráfico salvo: 'execution_times_comparison.png'")
    plt.show()


def plot_speedup_analysis(par_results, dist_results):
    """Gráfico de speedup."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Speedup paralelo
    if par_results:
        ax = axes[0]
        grid_sizes = par_results['grid_sizes']
        
        for grid_size in grid_sizes:
            if str(grid_size) in par_results['speedups']:
                thread_counts = sorted([int(k) for k in par_results['speedups'][str(grid_size)].keys()])
                speedups = [par_results['speedups'][str(grid_size)][str(tc)] for tc in thread_counts]
                
                ax.plot(thread_counts, speedups, 'o-', linewidth=2, markersize=8,
                       label=f'Malha {grid_size}x{grid_size}')
        
        # Linha ideal
        max_threads = max(par_results['thread_counts'])
        ax.plot([1, max_threads], [1, max_threads], 'k--', linewidth=2, alpha=0.5, label='Speedup Ideal')
        
        ax.set_xlabel('Número de Threads', fontsize=12, fontweight='bold')
        ax.set_ylabel('Speedup', fontsize=12, fontweight='bold')
        ax.set_title('Speedup - Versão Paralela', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    # Speedup distribuído
    if dist_results:
        ax = axes[1]
        grid_sizes = dist_results['grid_sizes']
        
        for grid_size in grid_sizes:
            if str(grid_size) in dist_results['speedups']:
                worker_counts = sorted([int(k) for k in dist_results['speedups'][str(grid_size)].keys()])
                speedups = [dist_results['speedups'][str(grid_size)][str(wc)] for wc in worker_counts]
                
                ax.plot(worker_counts, speedups, 's-', linewidth=2, markersize=8,
                       label=f'Malha {grid_size}x{grid_size}')
        
        # Linha ideal
        max_workers = max(dist_results['worker_counts'])
        ax.plot([1, max_workers], [1, max_workers], 'k--', linewidth=2, alpha=0.5, label='Speedup Ideal')
        
        ax.set_xlabel('Número de Workers', fontsize=12, fontweight='bold')
        ax.set_ylabel('Speedup', fontsize=12, fontweight='bold')
        ax.set_title('Speedup - Versão Distribuída', fontsize=13, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('speedup_analysis.png', dpi=300)
    print("Gráfico salvo: 'speedup_analysis.png'")
    plt.show()


def calculate_efficiency(par_results, dist_results):
    """Calcula e exibe eficiência de paralelização."""
    print("\n" + "=" * 80)
    print("ANÁLISE DE EFICIÊNCIA")
    print("=" * 80)
    
    if par_results:
        print("\n--- VERSÃO PARALELA ---")
        for grid_size in par_results['grid_sizes']:
            print(f"\nMalha {grid_size}x{grid_size}:")
            
            if str(grid_size) in par_results['speedups']:
                for num_threads in sorted([int(k) for k in par_results['speedups'][str(grid_size)].keys()]):
                    speedup = par_results['speedups'][str(grid_size)][str(num_threads)]
                    efficiency = (speedup / num_threads) * 100
                    print(f"  {num_threads} threads: Speedup={speedup:.2f}x, Eficiência={efficiency:.1f}%")
    
    if dist_results:
        print("\n--- VERSÃO DISTRIBUÍDA ---")
        for grid_size in dist_results['grid_sizes']:
            print(f"\nMalha {grid_size}x{grid_size}:")
            
            if str(grid_size) in dist_results['speedups']:
                for num_workers in sorted([int(k) for k in dist_results['speedups'][str(grid_size)].keys()]):
                    speedup = dist_results['speedups'][str(grid_size)][str(num_workers)]
                    efficiency = (speedup / num_workers) * 100
                    print(f"  {num_workers} workers: Speedup={speedup:.2f}x, Eficiência={efficiency:.1f}%")
    
    print("=" * 80)


def generate_report(seq_results, par_results, dist_results):
    """Gera relatório completo em markdown."""
    with open('performance_report.md', 'w', encoding='utf-8') as f:
        f.write("# Relatório de Desempenho: Difusão de Calor 2D\n\n")
        f.write("## Configurações do Sistema\n\n")
        f.write("- **Problema**: Equação de difusão de calor 2D\n")
        f.write("- **Método numérico**: Diferenças finitas (FTCS)\n")
        f.write("- **Linguagem**: Python 3.x\n")
        f.write("- **Paralelização**: Threading (threads) e Sockets (distribuído)\n\n")
        
        f.write("## Resultados\n\n")
        f.write("### Tempos de Execução\n\n")
        
        if seq_results:
            f.write("| Tamanho Malha | Sequencial (s) | Iterações |\n")
            f.write("|---------------|----------------|----------|\n")
            
            for i, gs in enumerate(seq_results['grid_sizes']):
                f.write(f"| {gs}x{gs} | {seq_results['times'][i]:.4f} | {seq_results['iterations'][i]:.0f} |\n")
        
        f.write("\n### Análise de Speedup\n\n")
        f.write("**Speedup** é definido como: `Speedup = Tempo_Sequencial / Tempo_Paralelo`\n\n")
        f.write("**Eficiência** é definida como: `Eficiência = Speedup / Número_de_Recursos * 100%`\n\n")
        
        f.write("\n## Conclusões\n\n")
        f.write("1. **Escalabilidade**: Analisar como o desempenho varia com tamanho do problema\n")
        f.write("2. **Eficiência de Paralelização**: Comparar speedup real vs. ideal\n")
        f.write("3. **Overhead de Comunicação**: Versão distribuída tem maior overhead\n")
        f.write("4. **Lei de Amdahl**: Limitações de paralelização devido a regiões sequenciais\n\n")
        
        f.write("## Limitações Identificadas\n\n")
        f.write("- **GIL (Global Interpreter Lock)**: Limita paralelismo real em threads Python\n")
        f.write("- **Overhead de comunicação**: Sockets introduzem latência\n")
        f.write("- **Sincronização**: Barreiras entre threads adicionam overhead\n")
        f.write("- **Cache**: Acesso não-localizado à memória reduz performance\n\n")
        
        f.write("## Melhorias Propostas\n\n")
        f.write("1. **Usar multiprocessing em vez de threading** para evitar GIL\n")
        f.write("2. **Implementar em NumPy vetorizado** para melhor performance sequencial\n")
        f.write("3. **Usar MPI (mpi4py)** para comunicação distribuída mais eficiente\n")
        f.write("4. **Compilar com Numba/Cython** para acelerar loops críticos\n")
        f.write("5. **Implementar em GPU com CUDA/OpenCL** para problemas grandes\n")
    
    print("Relatório salvo: 'performance_report.md'")


if __name__ == "__main__":
    seq_results, par_results, dist_results = load_results()
    
    if seq_results:
        create_comparison_table(seq_results, par_results, dist_results)
        plot_execution_times(seq_results, par_results, dist_results)
    
    if par_results or dist_results:
        plot_speedup_analysis(par_results, dist_results)
        calculate_efficiency(par_results, dist_results)
    
    generate_report(seq_results, par_results, dist_results)
    
    print("\n✅ Análise completa!")
