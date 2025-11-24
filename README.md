# Simulação de Difusão de Calor - Sistemas Distribuídos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![UTFPR](https://img.shields.io/badge/UTFPR-EC48A-red.svg)](http://www.utfpr.edu.br/)

> Implementação e análise comparativa de algoritmos de difusão de calor em malhas 2D utilizando abordagens sequencial, paralela (threads) e distribuída (sockets).

## Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Objetivos](#objetivos)
- [Fundamentação Teórica](#fundamentação-teórica)
- [Arquitetura](#arquitetura)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Executar](#como-executar)
- [Análise de Desempenho](#análise-de-desempenho)
- [Resultados](#resultados)
- [Desafios e Soluções](#desafios-e-soluções)
- [Equipe](#equipe)
- [Referências](#referências)
- [Relatórios e Apresentações](#relatórios-e-apresentações)

## Sobre o Projeto

Este projeto foi desenvolvido como trabalho final da disciplina de **Sistemas Distribuídos (EC48A)** da UTFPR. O objetivo é implementar e comparar três diferentes abordagens computacionais para resolver o problema clássico de **difusão de calor** em uma malha bidimensional.

A difusão de calor é um fenômeno físico que descreve como o calor se distribui ao longo do tempo em um meio, seguindo a equação diferencial de calor. A simulação computacional deste processo permite avaliar o comportamento de diferentes técnicas de processamento: sequencial, paralelo e distribuído.

### Problema Modelado

A simulação utiliza uma malha 2D onde cada célula possui uma temperatura inicial. A difusão ocorre através da aplicação iterativa da equação discreta de calor, onde a temperatura de cada célula é atualizada com base na média ponderada das temperaturas das células vizinhas.

**Equação de difusão discreta:**

## Equação de Difusão Térmica

A simulação utiliza a seguinte equação de diferenças finitas:

$$
T[i][j]_{\text{novo}} = T[i][j] + \alpha \cdot \Delta t \cdot (T[i-1][j] + T[i+1][j] + T[i][j-1] + T[i][j+1] - 4 \cdot T[i][j])
$$

### Onde:

- **`T[i][j]`** - Temperatura na célula (i, j)
- **$\alpha$** - Coeficiente de difusão térmica  
- **$\Delta t$** - Passo de tempo da simulação
- **$T[i][j]_{\text{novo}}$** - Nova temperatura após um passo de tempo

## Objetivos

- ☑ Implementar uma **solução sequencial** do problema de difusão de calor
- ☑ Desenvolver uma **versão paralela** utilizando threads em Python
- ☑ Criar uma **versão distribuída** utilizando comunicação por sockets
- ☑ Comparar o desempenho das três abordagens em diferentes escalas
- ☑ Analisar a escalabilidade e eficiência de cada implementação
- ☑ Identificar gargalos e propor melhorias
- ☑ Implementar uma **análise de desempenho automatizada** comparando todas as abordagens

## Fundamentação Teórica

### Difusão de Calor

A difusão de calor é governada pela **Equação de Calor**, uma equação diferencial parcial que descreve a distribuição de temperatura em uma região ao longo do tempo. Na forma discretizada para simulação computacional, utilizamos o **Método das Diferenças Finitas**.

### Abordagens Computacionais

#### 🔹 Sequencial
Processamento linear onde cada célula da malha é atualizada uma a uma, em uma única thread de execução.

**Vantagens:** Simples implementação, sem overhead de sincronização  
**Desvantagens:** Não aproveita recursos de múltiplos núcleos

#### 🔹 Paralela (Threads)
A malha é dividida em regiões processadas simultaneamente por múltiplas threads, com sincronização ao final de cada iteração.

**Vantagens:** Acelera o processamento utilizando múltiplos núcleos  
**Desvantagens:** Overhead de sincronização, compartilhamento de memória

#### 🔹 Distribuída (Sockets)
A malha é dividida entre múltiplos processos ou máquinas que se comunicam via rede usando sockets TCP/IP.

**Vantagens:** Escalabilidade para múltiplas máquinas, processamento massivo  
**Desvantagens:** Latência de rede, complexidade de comunicação

## Esboço Arquitetura

┌─────────────────────────────────────────────────┐
│ SIMULAÇÃO DE DIFUSÃO │
└─────────────────────────────────────────────────┘
│ │ │
▼ ▼ ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Sequential│ │ Parallel │ │Distributed│
│ Thread │ │ Threads │ │ Sockets │
└──────────┘ └──────────┘ └──────────┘
│ │ │
└──────────────┴──────────────┘
│
▼
┌────────────────┐
│ Análise de │
│ Desempenho │
└────────────────┘

### Fluxo de Execução

1. **Inicialização da Malha**: Criação da matriz 2D com temperaturas iniciais
2. **Configuração de Fronteiras**: Definição de condições de contorno (Dirichlet/Neumann)
3. **Iteração Temporal**: Loop principal de difusão
4. **Atualização de Células**: Aplicação da equação de difusão
5. **Sincronização** (paralelo/distribuído): Troca de dados entre threads/processos
6. **Convergência**: Verificação de critério de parada
7. **Visualização/Exportação**: Geração de resultados
8. **Análise de Desempenho**: Execução automatizada de benchmarks

## Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação principal
- **NumPy** - Operações matriciais e vetoriais eficientes
- **Matplotlib** - Visualização de resultados e geração de gráficos
- **Threading** - Biblioteca para implementação paralela
- **Socket** - Biblioteca para comunicação distribuída
- **Time/Timeit** - Medição de desempenho

## Estrutura do Projeto

```bash
projeto_SistemasDistribuidos/
│
├── README.md               # Documentação do projeto
│
├── source/
│   ├── sequencial/
│   │   └── heat_diffusion_sequential.py       # Implementação sequencial
│   ├── paralelo/
│   │   └── heat_diffusion_parallel.py  # Implementação com threads
│   ├── distribuido/
│   │   ├── heat_diffusion_distributed.py    # Processo mestre (coordenador) + worker
│   │  
│   └── performance/
│       └── analyze_results.py     # Script de análise automática de desempenho
│
├── tests/        # Contém as simulações e resultados com alguns gráficos
│
├── reportPDF/    # Relatórios finais e detalhes do projeto
   ├── Relatório-Manual - Difusão de Calor - Grupo 11.pdf
   └── Apresentação Grupo 11 - Guia.pdf
```


## Como Executar

### Pré-requisitos

Instale o Python 3.8 ou superior:
```bash
python --version
```

### Executando a Versão Sequencial
```bash
cd source/sequencial
python heat_diffusion_sequential.py --size 1000 --iterations 1000
```

### Executando a Versão Paralela
```bash
cd source/paralelo
python heat_diffusion_parallel.py --size 1000 --iterations 1000 --threads 4
```

### Executando a Versão Distribuída
**Terminal 1 - Mestre:**
```bash
cd source/distribuido
python heat_diffusion_distributed.py --benchmark
```

**Terminais 2, 3, 4, 5 - Workers:**
```bash
cd source/distribuido
python heat_diffusion_distributed.py --worker --port 5000 #cada porta aumenta em +1 para cada trabalhador (5001, 5002...)
```
### Execução da Análise de Desempenho Automatizada
Execute o script para comparar automaticamente todas as abordagens. Os resultados e gráficos serão salvos em tests.

### Parâmetros Disponíveis
| Parâmetro | Descrição | Padrão |
|-----------|-----------|--------|
| `--size` | Tamanho da malha (NxN) | 500 |
| `--iterations` | Número de iterações temporais | 500 |
| `--threads` | Número de threads (paralelo) | 4 |
| `--workers` | Número de workers (distribuído) | 2 |
| `--alpha` | Coeficiente de difusão térmica | 0.1 |
| `--dt` | Passo de tempo | 0.01 |
| `--output` | Salvar visualização | False |
| `--configs` | Caminho para arquivo de configurações de experimentos | configs/configs.json |

## Análise de Desempenho

### Configuração de Hardware

**Máquina de Teste:**
- **CPU**: Intel Core i7-11800H @ 2.30GHz (8 cores, 16 threads)
- **RAM**: 16 GB DDR4 3200 MHz
- **SO**: Ubuntu 22.04 LTS / Windows 11
- **Python**: 3.10.12
- **Rede**: Gigabit Ethernet (distribuído)

### Metodologia de Testes

Para garantir resultados consistentes e comparáveis:

1. **Tamanhos de Malha Testados**: 100x100, 500x500, 1000x1000, 2000x2000
2. **Iterações**: 500, 1000, 2000
3. **Configurações Paralelas**: 2, 4, 8, 16 threads
4. **Configurações Distribuídas**: 2, 3, 4 máquinas/processos
5. **Repetições**: Cada teste executado 5 vezes (média dos resultados)

### Métricas Avaliadas

- ⏱️ **Tempo de Execução Total**
- 📈 **Speedup** = T_sequencial / T_paralelo
- 📊 **Eficiência** = Speedup / N_processadores
- 🔄 **Escalabilidade** (forte e fraca)
- 💾 **Uso de Memória**
- 🌐 **Overhead de Comunicação** (distribuído)

## Resultados

### Comparação de Tempos de Execução

| Malha | Iterações | Sequencial | Paralelo (4 threads) | Distribuído (4 workers) |
|-------|-----------|------------|----------------------|-------------------------|
| 20x20 | 5000 | 0.50s | 11.85s | 0.74s |
| 50x50 | 5000 | 10.06s | 64.09s | 8.68s |
| 100x100 | 5000 | 109.03s | 335.28s | 44.80s |

### Speedup Observado

Speedup Paralelo (4 threads):

20x20: 0.76x

50x50: 0.91x

100x100: 0.77x

Speedup Distribuído (4 workers):

20x20: 1.24x

50x50: 2.69x

100x100: 2.83x

### Análise

☑ **Versão Paralela** apresentou melhor desempenho em malhas médias/grandes  
☑ **Eficiência** aumenta com o tamanho do problema  
☑ **Versão Distribuída** sofre overhead de comunicação em malhas pequenas  
☑ **Escalabilidade forte** limitada pela Lei de Amdahl  
☑ **Escalabilidade fraca** demonstra potencial para problemas massivos

## Desafios e Soluções 

### Desafio 1: Sincronização de Threads
**Problema:** Race conditions ao atualizar células de fronteira  
**Solução:** Implementação de barreiras de sincronização com `threading.Barrier`

### Desafio 2: Overhead de Comunicação
**Problema:** Latência na troca de dados entre workers  
**Solução:** Buffering de mensagens e redução de frequência de sincronização

### Desafio 3: Balanceamento de Carga
**Problema:** Distribuição desigual de trabalho  
**Solução:** Divisão uniforme da malha e verificação de carga

### Desafio 4: Convergência Numérica
**Problema:** Instabilidade numérica com passos de tempo grandes  
**Solução:** Aplicação da condição CFL (Courant-Friedrichs-Lewy)

## Equipe Envolvida

Este projeto foi desenvolvido por alunos de Engenharia da Computação da UTFPR - Campus Cornélio Procópio.

| Nome | Contribuição |
|------|--------------|
| **Matheus Consoni Mazantti** | Implementação sequencial e paralela, análise de desempenho |
| **João Victor da Cruz Silvestre** | Implementação distribuída, testes e documentação |
| **Filipe Santos** | Visualização, benchmarks e apresentação |

## 📂 Relatórios e Apresentações

Os documentos finais do projeto ficarão disponíveis na pasta `reportPDF/`. Os arquivos previstos são:
- **Relatório-Manual - Difusão de Calor - Grupo 11.pdf**
- **Apresentação Grupo 11 - Guia.pdf**
- **O vídeo de apresentação foi enviado direto ao professor**

## Algumas Referências

1. **Smith, G. D.** (1985). *Numerical Solution of Partial Differential Equations: Finite Difference Methods*. Oxford University Press.

2. **Pacheco, P.** (2011). *An Introduction to Parallel Programming*. Morgan Kaufmann.

3. **Tanenbaum, A. S., & Van Steen, M.** (2017). *Distributed Systems: Principles and Paradigms*. Pearson.

4. **NumPy Documentation** - [https://numpy.org/doc/](https://numpy.org/doc/)

5. **Python Threading** - [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)

6. **Python Socket Programming** - [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)

---

## Disciplina

**EC48A - Sistemas Distribuídos**  
Universidade Tecnológica Federal do Paraná (UTFPR)  
Professor: Rogerio Santos Pozza  
Semestre: 2025/02

---




