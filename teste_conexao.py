import MetaTrader5 as mt5
import sys

print("="*50)
print("🔍 DIAGNÓSTICO DE CONEXÃO MT5")
print("="*50)

# Caminho exato do MT5
MT5_PATH = r"C:\Program Files\MetaTrader 5\terminal64.exe"

print("\n📦 Passo 1: Verificando biblioteca MT5...")
print(f"Versão da biblioteca: {mt5.__version__}")

print("\n🔌 Passo 2: Inicializando conexão com MT5...")
if not mt5.initialize(path=MT5_PATH):
    erro = mt5.last_error()
    print(f"❌ Falha ao inicializar!")
    print(f"Código do erro: {erro[0]}")
    print(f"Mensagem: {erro[1]}")
    sys.exit()
else:
    print("✅ MT5 inicializado com sucesso!")

print("\n🔑 Passo 3: Tentando login...")
LOGIN    = 105200600#LOGIN DE CONTA
SENHA    = "SUA_SENHA_AQUI"
SERVIDOR = "MetaQuotes-Demo" #SERVIDOR

autorizado = mt5.login(LOGIN, password=SENHA, server=SERVIDOR)

if not autorizado:
    erro = mt5.last_error()
    print(f"❌ Falha no login!")
    print(f"Código: {erro[0]} | Mensagem: {erro[1]}")
else:
    info = mt5.account_info()
    print("✅ Login realizado com sucesso!")
    print("\n" + "="*50)
    print("🏦 DADOS DA CONTA:")
    print(f"  Nome    : {info.name}")
    print(f"  Login   : {info.login}")
    print(f"  Saldo   : ${info.balance}")
    print(f"  Servidor: {info.server}")
    print(f"  Moeda   : {info.currency}")
    print("="*50)

mt5.shutdown()
print("\n🔒 Conexão encerrada.")