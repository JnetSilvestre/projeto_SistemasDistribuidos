# 🔥 Simulação de Difusão de Calor - Sistemas Distribuídos

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UTFPR](https://img.shields.io/badge/UTFPR-EC48A-red.svg)](http://www.utfpr.edu.br/)

> Implementação e análise comparativa de algoritmos de difusão de calor em malhas 2D utilizando abordagens sequencial, paralela (threads) e distribuída (sockets).

## 📋 Sumário

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

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como trabalho final da disciplina de **Sistemas Distribuídos (EC48A)** da UTFPR. O objetivo é implementar e comparar três diferentes abordagens computacionais para resolver o problema clássico de **difusão de calor** em uma malha bidimensional.

A difusão de calor é um fenômeno físico que descreve como o calor se distribui ao longo do tempo em um meio, seguindo a equação diferencial de calor. A simulação computacional deste processo permite avaliar o comportamento de diferentes técnicas de processamento: sequencial, paralelo e distribuído.

### 🔍 Problema Modelado

A simulação utiliza uma malha 2D onde cada célula possui uma temperatura inicial. A difusão ocorre através da aplicação iterativa da equação discreta de calor, onde a temperatura de cada célula é atualizada com base na média ponderada das temperaturas das células vizinhas.

**Equação de difusão discreta:**

T[i][j]_novo = T[i][j] + α * Δt * (T[i-1][j] + T[i+1][j] + T[i][j-1] + T[i][j+1] - 4*T[i][j])


Onde:
- `T[i][j]` é a temperatura na célula (i, j)
- `α` é o coeficiente de difusão térmica
- `Δt` é o passo de tempo da simulação

## 🎯 Objetivos

- ✅ Implementar uma **solução sequencial** do problema de difusão de calor
- ✅ Desenvolver uma **versão paralela** utilizando threads em Python
- ✅ Criar uma **versão distribuída** utilizando comunicação por sockets
- 📊 Comparar o desempenho das três abordagens em diferentes escalas
- 📈 Analisar a escalabilidade e eficiência de cada implementação
- 🔧 Identificar gargalos e propor melhorias

## 📚 Fundamentação Teórica

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

## 🏗️ Arquitetura

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

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem de programação principal
- **NumPy** - Operações matriciais e vetoriais eficientes
- **Matplotlib** - Visualização de resultados e geração de gráficos
- **Threading** - Biblioteca para implementação paralela
- **Socket** - Biblioteca para comunicação distribuída
- **Time/Timeit** - Medição de desempenho

## 📁 Estrutura do Projeto

projeto_SistemasDistribuidos/
│
├── README.md # Documentação do projeto
├── requirements.txt # Dependências Python
│
├── sequencial/
│ └── heat_diffusion_seq.py # Implementação sequencial
│
├── paralelo/
│ └── heat_diffusion_parallel.py # Implementação com threads
│
├── distribuido/
│ ├── heat_diffusion_master.py # Processo mestre (coordenador)
│ └── heat_diffusion_worker.py # Processo worker (trabalhador)
│
├── utils/
│ ├── visualization.py # Funções de visualização
│ └── benchmark.py # Scripts de medição de desempenho
│
├── results/
│ ├── graphs/ # Gráficos de desempenho
│ └── tables/ # Tabelas comparativas
│
└── docs/
└── apresentacao.pdf # Apresentação do trabalho


## 🚀 Como Executar

### Pré-requisitos

Python 3.8 ou superior
python --version

Instalar dependências
pip install -r requirements.txt


### Executando a Versão Sequencial
cd sequencial
python heat_diffusion_seq.py --size 1000 --iterations 1000

### Executando a Versão Paralela
cd paralelo
python heat_diffusion_parallel.py --size 1000 --iterations 1000 --threads 4


### Executando a Versão Distribuída

**Terminal 1 - Mestre:**
cd distribuido
python heat_diffusion_master.py --size 1000 --iterations 1000 --workers 3

**Terminais 2, 3, 4 - Workers:**
cd distribuido
python heat_diffusion_worker.py --host localhost --port 5000


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

## 📊 Análise de Desempenho

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

## 📈 Resultados

### Comparação de Tempos de Execução

| Malha | Iterações | Sequencial | Paralelo (4 threads) | Distribuído (3 workers) |
|-------|-----------|------------|----------------------|-------------------------|
| 100x100 | 500 | 0.45s | 0.18s | 0.35s |
| 500x500 | 1000 | 12.3s | 3.7s | 5.2s |
| 1000x1000 | 1000 | 48.6s | 13.2s | 16.8s |
| 2000x2000 | 2000 | 385.4s | 98.5s | 112.3s |

### Speedup Observado

Speedup Paralelo (4 threads):

100x100: 2.5x

500x500: 3.3x

1000x1000: 3.7x

2000x2000: 3.9x

Speedup Distribuído (3 workers):

100x100: 1.3x

500x500: 2.4x

1000x1000: 2.9x

2000x2000: 3.4x


### Análise

✅ **Versão Paralela** apresentou melhor desempenho em malhas médias/grandes  
✅ **Eficiência** aumenta com o tamanho do problema  
⚠️ **Versão Distribuída** sofre overhead de comunicação em malhas pequenas  
⚠️ **Escalabilidade forte** limitada pela Lei de Amdahl  
✅ **Escalabilidade fraca** demonstra potencial para problemas massivos

## 🔧 Desafios e Soluções

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

## 👥 Equipe

Este projeto foi desenvolvido por alunos de Engenharia da Computação da UTFPR - Campus Curitiba.

| Nome | Contribuição |
|------|--------------|
| **[Matheus Consoni Mazantti]** | Implementação sequencial e paralela, análise de desempenho |
| **[João Victor da Cruz Silvestre]** | Implementação distribuída, testes e documentação |
| **[Filipe Santos]** | Visualização, benchmarks e apresentação |

## 📚 Algumas Referências

1. **Smith, G. D.** (1985). *Numerical Solution of Partial Differential Equations: Finite Difference Methods*. Oxford University Press.

2. **Pacheco, P.** (2011). *An Introduction to Parallel Programming*. Morgan Kaufmann.

3. **Tanenbaum, A. S., & Van Steen, M.** (2017). *Distributed Systems: Principles and Paradigms*. Pearson.

4. **NumPy Documentation** - [https://numpy.org/doc/](https://numpy.org/doc/)

5. **Python Threading** - [https://docs.python.org/3/library/threading.html](https://docs.python.org/3/library/threading.html)

6. **Python Socket Programming** - [https://docs.python.org/3/library/socket.html](https://docs.python.org/3/library/socket.html)

---

## 🎓 Disciplina

**EC48A - Sistemas Distribuídos**  
Universidade Tecnológica Federal do Paraná (UTFPR)  
Professor: [Rogerio Santos Pozza]  
Semestre: 2025/02

---




