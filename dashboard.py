import streamlit as st
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time

# ============================================================
# CONFIGURAÇÕES — edite aqui
# ============================================================
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"
LOGIN    = 105222646 #CONTA
SENHA    = "SUA_SENHA_AQUI" #SENHA
SERVIDOR = "MetaQuotes-Demo" #SERVER

ATIVOS = ["EURUSD", "GBPUSD", "USDJPY", "EURGBP", "USDCHF", "EURJPY"]

# ============================================================
# PÁGINA
# ============================================================
st.set_page_config(
    page_title="Robô Visão Noturna",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        background-color: #0a0e1a;
        color: #e0e8ff;
    }
    .stApp { background-color: #0a0e1a; }

    .metric-card {
        background: linear-gradient(135deg, #0f1629 0%, #141c35 100%);
        border: 1px solid #1e2d5a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,120,255,0.1);
    }
    .metric-label {
        font-size: 12px;
        color: #4a6fa5;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-family: 'Share Tech Mono', monospace;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #00d4ff;
        font-family: 'Share Tech Mono', monospace;
    }
    .metric-value.green { color: #00ff88; }
    .metric-value.red   { color: #ff4466; }

    .section-title {
        font-size: 14px;
        color: #4a6fa5;
        text-transform: uppercase;
        letter-spacing: 3px;
        border-bottom: 1px solid #1e2d5a;
        padding-bottom: 8px;
        margin-bottom: 16px;
        font-family: 'Share Tech Mono', monospace;
    }
    .status-dot {
        display: inline-block;
        width: 10px; height: 10px;
        border-radius: 50%;
        background: #00ff88;
        box-shadow: 0 0 8px #00ff88;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }
    header { visibility: hidden; }
    .stDataFrame { background: #0f1629 !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONEXÃO
# ============================================================
@st.cache_resource
def conectar_mt5():
    if not mt5.initialize(path=MT5_PATH):
        return False
    if not mt5.login(LOGIN, password=SENHA, server=SERVIDOR):
        return False
    return True

# ============================================================
# DADOS
# ============================================================
def get_account_info():
    info = mt5.account_info()
    if info is None:
        return None
    return {
        "nome"   : info.name,
        "login"  : info.login,
        "saldo"  : info.balance,
        "equity" : info.equity,
        "lucro"  : info.profit,
        "margem" : info.margin_free,
        "moeda"  : info.currency,
        "servidor": info.server
    }

def get_ordens_abertas():
    posicoes = mt5.positions_get()
    if posicoes is None or len(posicoes) == 0:
        return pd.DataFrame()
    dados = []
    for p in posicoes:
        dados.append({
            "Ativo"  : p.symbol,
            "Tipo"   : "BUY" if p.type == 0 else "SELL",
            "Volume" : p.volume,
            "Preço Abertura": p.price_open,
            "Preço Atual"   : p.price_current,
            "SL"     : p.sl,
            "TP"     : p.tp,
            "Lucro"  : p.profit,
            "Abertura": datetime.fromtimestamp(p.time).strftime("%d/%m %H:%M")
        })
    return pd.DataFrame(dados)

def get_historico(dias=7):
    inicio = datetime.now() - timedelta(days=dias)
    deals  = mt5.history_deals_get(inicio, datetime.now())
    if deals is None or len(deals) == 0:
        return pd.DataFrame()
    dados = []
    for d in deals:
        if d.entry == 1:  # apenas fechamentos
            dados.append({
                "Ativo"  : d.symbol,
                "Tipo"   : "BUY" if d.type == 0 else "SELL",
                "Volume" : d.volume,
                "Preço"  : d.price,
                "Lucro"  : d.profit,
                "Data"   : datetime.fromtimestamp(d.time).strftime("%d/%m %H:%M")
            })
    return pd.DataFrame(dados)

def get_pnl_por_ativo(hist_df):
    if hist_df.empty:
        return pd.DataFrame()
    return hist_df.groupby("Ativo")["Lucro"].sum().reset_index().sort_values("Lucro", ascending=False)

# ============================================================
# INTERFACE
# ============================================================
conectado = conectar_mt5()

# Header
col_title, col_status = st.columns([3, 1])
with col_title:
    st.markdown("# 🤖 Robô Visão Noturna")
    st.markdown("**Os 6 Magníficos** — EURUSD · GBPUSD · USDJPY · EURGBP · USDCHF · EURJPY")
with col_status:
    if conectado:
        st.markdown('<div style="text-align:right;padding-top:20px"><span class="status-dot"></span><span style="color:#00ff88;font-size:14px">CONECTADO</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:right;padding-top:20px"><span style="color:#ff4466;font-size:14px">❌ DESCONECTADO</span></div>', unsafe_allow_html=True)

st.markdown("---")

if not conectado:
    st.error("❌ Não foi possível conectar ao MT5. Verifique se o terminal está aberto e as credenciais estão corretas.")
    st.stop()

# Dados
info    = get_account_info()
abertas = get_ordens_abertas()
hist    = get_historico(dias=30)
pnl     = get_pnl_por_ativo(hist)

# ── Métricas principais ──────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Saldo</div>
        <div class="metric-value">${info['saldo']:,.2f}</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 Equity</div>
        <div class="metric-value">${info['equity']:,.2f}</div>
    </div>""", unsafe_allow_html=True)

with c3:
    cor   = "green" if info['lucro'] >= 0 else "red"
    sinal = "+" if info['lucro'] >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📈 Lucro Aberto</div>
        <div class="metric-value {cor}">{sinal}${info['lucro']:,.2f}</div>
    </div>""", unsafe_allow_html=True)

with c4:
    total_hist = hist["Lucro"].sum() if not hist.empty else 0
    cor2   = "green" if total_hist >= 0 else "red"
    sinal2 = "+" if total_hist >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏆 Lucro Total (30d)</div>
        <div class="metric-value {cor2}">{sinal2}${total_hist:,.2f}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Ordens abertas ───────────────────────────────────────────
st.markdown('<div class="section-title">⚡ Posições Abertas</div>', unsafe_allow_html=True)

if abertas.empty:
    st.info("😴 Nenhuma posição aberta no momento — robô aguardando sinal.")
else:
    def colorir(val):
        if isinstance(val, float):
            color = "#00ff88" if val > 0 else "#ff4466" if val < 0 else "white"
            return f"color: {color}"
        return ""
    st.dataframe(
        abertas.style.applymap(colorir, subset=["Lucro"]),
        use_container_width=True,
        hide_index=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── Gráfico + PnL por ativo ─────────────────────────────────
col_chart, col_pnl = st.columns([2, 1])

with col_chart:
    st.markdown('<div class="section-title">📈 Performance (últimos 30 dias)</div>', unsafe_allow_html=True)
    if not hist.empty:
        hist["Data_dt"] = pd.to_datetime(hist["Data"], format="%d/%m %H:%M", errors="coerce")
        hist_sorted = hist.sort_values("Data_dt")
        hist_sorted["Lucro Acumulado"] = hist_sorted["Lucro"].cumsum()
        st.line_chart(hist_sorted.set_index("Data")["Lucro Acumulado"], use_container_width=True)
    else:
        st.info("Sem histórico de operações ainda.")

with col_pnl:
    st.markdown('<div class="section-title">💎 P&L por Ativo</div>', unsafe_allow_html=True)
    if not pnl.empty:
        for _, row in pnl.iterrows():
            cor = "#00ff88" if row["Lucro"] >= 0 else "#ff4466"
            sinal = "+" if row["Lucro"] >= 0 else ""
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        padding:8px 12px;margin-bottom:6px;
                        background:#0f1629;border-radius:8px;
                        border-left:3px solid {cor}">
                <span style="font-weight:600">{row['Ativo']}</span>
                <span style="color:{cor};font-family:'Share Tech Mono',monospace">
                    {sinal}${row['Lucro']:.2f}
                </span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Sem dados ainda.")

st.markdown("<br>", unsafe_allow_html=True)

# ── Histórico ────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Histórico de Operações (30 dias)</div>', unsafe_allow_html=True)
if not hist.empty:
    st.dataframe(
        hist[["Data","Ativo","Tipo","Volume","Preço","Lucro"]].sort_values("Data", ascending=False).style.applymap(
            lambda v: f"color: {'#00ff88' if v > 0 else '#ff4466'}" if isinstance(v, float) else "",
            subset=["Lucro"]
        ),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Nenhuma operação fechada nos últimos 30 dias.")

# ── Rodapé + Auto-refresh ────────────────────────────────────
st.markdown("---")
col_footer, col_refresh = st.columns([3,1])
with col_footer:
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.markdown(f'<span style="color:#4a6fa5;font-size:12px;font-family:monospace">Última atualização: {agora} | Conta: {info["login"]} | {info["servidor"]}</span>', unsafe_allow_html=True)
with col_refresh:
    if st.button("🔄 Atualizar", use_container_width=True):
        st.rerun()

# Auto-refresh a cada 30 segundos
time.sleep(30)
st.rerun()