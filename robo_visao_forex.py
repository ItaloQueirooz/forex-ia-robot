import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURAÇÕES
# ============================================================
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
LOGIN    = 5048650522 #LOGIN DE CONTA
SENHA    = "SUA-SENHA-AQUI"
SERVIDOR = "MetaQuotes-Demo" #SERVIDOR

ATIVOS = ["EURUSD", "GBPUSD", "USDJPY", "EURGBP", "USDCHF", "EURJPY"]

CONFIG = {
    "volume"       : 0.01,   # lote mínimo (seguro para demo)
    "stop_loss_pts": 50,     # 50 pontos de stop loss
    "take_profit_pts": 100,  # 100 pontos de take profit
    "intervalo_hrs": 3,      # trava de 3 horas entre operações
    "timeframe"    : mt5.TIMEFRAME_H1
}

ultimas_operacoes = {ativo: None for ativo in ATIVOS}

# ============================================================
# CONEXÃO
# ============================================================
def conectar():
    if not mt5.initialize(path=MT5_PATH):
        print(f"❌ Erro ao inicializar: {mt5.last_error()}")
        return False
    if not mt5.login(LOGIN, password=SENHA, server=SERVIDOR):
        print(f"❌ Erro no login: {mt5.last_error()}")
        return False
    info = mt5.account_info()
    print(f"✅ Conectado | {info.name} | Saldo: ${info.balance:,.2f}")
    return True

# ============================================================
# SINAL (MÉDIAS MÓVEIS + RSI)
# ============================================================
def calcular_sinal(ativo):
    barras = mt5.copy_rates_from_pos(ativo, CONFIG["timeframe"], 0, 100)
    if barras is None or len(barras) < 50:
        return None

    df = pd.DataFrame(barras)
    df["ma_rapida"] = df["close"].rolling(9).mean()
    df["ma_lenta"]  = df["close"].rolling(21).mean()

    # RSI
    delta = df["close"].diff()
    gain  = delta.where(delta > 0, 0).rolling(14).mean()
    loss  = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs    = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    ultima = df.iloc[-1]
    anterior = df.iloc[-2]

    compra  = anterior["ma_rapida"] < anterior["ma_lenta"] and ultima["ma_rapida"] > ultima["ma_lenta"] and ultima["rsi"] < 65
    venda   = anterior["ma_rapida"] > anterior["ma_lenta"] and ultima["ma_rapida"] < ultima["ma_lenta"] and ultima["rsi"] > 35

    if compra:
        return "BUY"
    elif venda:
        return "SELL"
    return None

# ============================================================
# ENVIAR ORDEM
# ============================================================
def enviar_ordem(ativo, direcao):
    symbol_info = mt5.symbol_info(ativo)
    if symbol_info is None:
        print(f"⚠️ {ativo} não encontrado")
        return False

    if not symbol_info.visible:
        mt5.symbol_select(ativo, True)

    tick = mt5.symbol_info_tick(ativo)
    point = symbol_info.point

    if direcao == "BUY":
        preco = tick.ask
        sl    = preco - CONFIG["stop_loss_pts"] * point
        tp    = preco + CONFIG["take_profit_pts"] * point
        tipo  = mt5.ORDER_TYPE_BUY
    else:
        preco = tick.bid
        sl    = preco + CONFIG["stop_loss_pts"] * point
        tp    = preco - CONFIG["take_profit_pts"] * point
        tipo  = mt5.ORDER_TYPE_SELL

    request = {
        "action"   : mt5.TRADE_ACTION_DEAL,
        "symbol"   : ativo,
        "volume"   : CONFIG["volume"],
        "type"     : tipo,
        "price"    : preco,
        "sl"       : sl,
        "tp"       : tp,
        "deviation": 20,
        "magic"    : 234000,
        "comment"  : "Visao Noturna",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    resultado = mt5.order_send(request)

    if resultado.retcode == mt5.TRADE_RETCODE_DONE:
        print(f"✅ {ativo} | {direcao} | Preço: {preco:.5f} | SL: {sl:.5f} | TP: {tp:.5f}")
        return True
    else:
        print(f"❌ {ativo} | Erro: {resultado.retcode} | {resultado.comment}")
        return False

# ============================================================
# VERIFICAR TRAVA DE 3 HORAS
# ============================================================
def pode_operar(ativo):
    ultima = ultimas_operacoes[ativo]
    if ultima is None:
        return True
    diferenca = (datetime.now() - ultima).total_seconds() / 3600
    return diferenca >= CONFIG["intervalo_hrs"]

# ============================================================
# LOOP PRINCIPAL
# ============================================================
def rodar():
    print("\n" + "="*50)
    print("🤖 ROBÔ VISÃO NOTURNA — 6 MAGNÍFICOS")
    print("="*50)

    if not conectar():
        return

    print(f"\n📊 Monitorando: {', '.join(ATIVOS)}")
    print("⏳ Verificando sinais a cada 60 segundos...\n")

    while True:
        agora = datetime.now().strftime("%H:%M:%S")
        print(f"\n🕐 [{agora}] Verificando mercado...")

        for ativo in ATIVOS:
            if not pode_operar(ativo):
                print(f"⏸️  {ativo} | Aguardando trava de 3h")
                continue

            sinal = calcular_sinal(ativo)

            if sinal:
                print(f"🎯 {ativo} | Sinal: {sinal}")
                sucesso = enviar_ordem(ativo, sinal)
                if sucesso:
                    ultimas_operacoes[ativo] = datetime.now()
            else:
                print(f"😴 {ativo} | Sem sinal")

        print(f"\n⏳ Próxima verificação em 60 segundos...")
        time.sleep(60)

# ============================================================
# INICIAR
# ============================================================
if __name__ == "__main__":
    rodar()
