# Relatório de Desempenho: Difusão de Calor 2D

## Configurações do Sistema

- **Problema**: Equação de difusão de calor 2D
- **Método numérico**: Diferenças finitas (FTCS)
- **Linguagem**: Python 3.x
- **Paralelização**: Threading (threads) e Sockets (distribuído)

## Resultados

### Tempos de Execução

| Tamanho Malha | Sequencial (s) | Iterações |
|---------------|----------------|----------|
| 20x20 | 0.5027 | 522 |
| 50x50 | 10.0678 | 1711 |
| 100x100 | 109.0307 | 4867 |

### Análise de Speedup

**Speedup** é definido como: `Speedup = Tempo_Sequencial / Tempo_Paralelo`

**Eficiência** é definida como: `Eficiência = Speedup / Número_de_Recursos * 100%`


## Conclusões

1. **Escalabilidade**: Analisar como o desempenho varia com tamanho do problema
2. **Eficiência de Paralelização**: Comparar speedup real vs. ideal
3. **Overhead de Comunicação**: Versão distribuída tem maior overhead
4. **Lei de Amdahl**: Limitações de paralelização devido a regiões sequenciais

## Limitações Identificadas

- **GIL (Global Interpreter Lock)**: Limita paralelismo real em threads Python
- **Overhead de comunicação**: Sockets introduzem latência
- **Sincronização**: Barreiras entre threads adicionam overhead
- **Cache**: Acesso não-localizado à memória reduz performance

## Melhorias Propostas

1. **Usar multiprocessing em vez de threading** para evitar GIL
2. **Implementar em NumPy vetorizado** para melhor performance sequencial
3. **Usar MPI (mpi4py)** para comunicação distribuída mais eficiente
4. **Compilar com Numba/Cython** para acelerar loops críticos
5. **Implementar em GPU com CUDA/OpenCL** para problemas grandes
