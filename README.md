# 🤖 forex-ia-robot — Visão Noturna

> Algoritmo quantitativo de negociação automatizada no mercado Forex, conectado ao MetaTrader 5 via API Python.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![MetaTrader5](https://img.shields.io/badge/MetaTrader-5-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Forward%20Testing-green?style=flat-square)
![Retorno](https://img.shields.io/badge/Backtest-7.7%25%20em%205%20meses-brightgreen?style=flat-square)

---

## 📌 Sobre o Projeto

O **forex-ia-robot** é um robô quantitativo desenvolvido em Python que opera automaticamente nos principais pares de moedas do mercado Forex. Ele utiliza cruzamento de médias móveis e RSI como filtro de entrada, com gestão de risco embutida e trava de tempo entre operações.

O projeto foi construído do zero, passando por backtesting, otimização de portfólio e forward testing em conta demo conectada ao MetaTrader 5.

---

## 📊 Resultados do Backtest

| Métrica | Resultado |
|---|---|
| Período testado | 5 meses (dados cegos) |
| Capital simulado | $10.000 |
| Lucro total | $770,80 |
| Retorno total | **7,7%** |
| Média mensal | **1,54% ao mês** |
| Equivalente anual | ~18,5% ao ano |

> 📈 18,5% ao ano supera o S&P 500 histórico (≈10,5% a.a.) e está em nível institucional (Hedge Fund).

---

## 🏦 Os 6 Magníficos — Portfólio Final

Após otimização baseada em dados (remoção de ativos com prejuízo sistemático):

| Par | Região | Motivo da Inclusão |
|---|---|---|
| EURUSD | Europa/EUA | Maior liquidez do mundo |
| GBPUSD | Reino Unido/EUA | Alta volatilidade controlada |
| USDJPY | EUA/Japão | Correlação asiática |
| EURGBP | Europa/Reino Unido | Correlação europeia |
| USDCHF | EUA/Suíça | Ativo refúgio |
| EURJPY | Europa/Japão | Cruzamento de alta liquidez |

---

## 🧠 Arquitetura do Código

```
forex-ia-robot/
│
├── robo_visao_noturna.py   # Robô principal (loop de execução)
├── teste_conexao.py        # Script de diagnóstico de conexão MT5
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação
```

### Fluxo de Decisão

```
Mercado (MT5)
     │
     ▼
Coleta 100 candles H1
     │
     ▼
Calcula MA9 + MA21 + RSI(14)
     │
     ▼
Cruzamento de médias?  ──NÃO──▶ 😴 Sem sinal
     │
    SIM
     │
     ▼
RSI confirma?  ──NÃO──▶ 😴 Filtrado
     │
    SIM
     │
     ▼
Envia ordem (BUY/SELL)
     │
     ▼
Trava 3 horas para o ativo
```

### Indicadores Utilizados

- **MA Rápida (9)** — Captura tendência de curto prazo
- **MA Lenta (21)** — Confirma tendência de médio prazo
- **RSI (14)** — Filtro de sobrecompra/sobrevenda (evita entradas em extremos)

### Gestão de Risco

| Parâmetro | Valor |
|---|---|
| Volume por operação | 0.01 lote (mínimo) |
| Stop Loss | 50 pontos |
| Take Profit | 100 pontos (RR 1:2) |
| Trava entre operações | 3 horas por ativo |

---

## 🚀 Guia de Instalação

### Pré-requisitos

- Windows 10/11
- Python 3.10
- MetaTrader 5 instalado ([download oficial](https://www.metatrader5.com/pt/download))
- Conta Demo na MetaQuotes (criada direto pelo MT5)

### Passo a Passo

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/forex-ia-robot.git
cd forex-ia-robot
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure suas credenciais**

Edite o arquivo `robo_visao_noturna.py` e substitua:
```python
LOGIN    = SEU_LOGIN
SENHA    = "SUA_SENHA"
SERVIDOR = "MetaQuotes-Demo"  # ou seu servidor
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
```

**4. Abra o MetaTrader 5** e certifique-se que está logado

**5. Rode o robô**
```bash
python robo_visao_noturna.py
```

---

## 📦 requirements.txt

```
MetaTrader5==5.0.5640
pandas
numpy
```

---

## ⚠️ Aviso de Risco

Este projeto é para fins educacionais e de pesquisa. Negociação no mercado Forex envolve risco de perda de capital. O desempenho passado (backtest) não garante resultados futuros. Sempre teste em conta demo antes de operar com dinheiro real.

---

## 🗺️ Roadmap

- [x] Desenvolvimento do algoritmo base
- [x] Backtesting em dados históricos (5 meses)
- [x] Otimização do portfólio (6 ativos)
- [x] Conexão com MetaTrader 5 via API Python
- [x] Forward Testing em conta demo
- [ ] Sistema de Copy Trading (sinais via Telegram)
- [ ] Dashboard de performance em tempo real
- [ ] Deploy em VPS para operação 24/7
- [ ] Mesa Proprietária (Prop Firm)

---

## 👨‍💻 Autor

**Italo Queiroz**
Analista de dados em formação 
---

## 📄 Licença

MIT License — sinta-se livre para estudar, modificar e distribuir.
