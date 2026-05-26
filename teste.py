from ofxparse import OfxParser
import pandas as pd

# Abre e processa o arquivo
with open("./Extrato Conta Corrente-2026.ofx", "rb") as arquivo:
    ofx = OfxParser.parse(arquivo)

# Lista para armazenar os dados do loop
dados_transacoes = []

for transacao in ofx.account.statement.transactions:
    dados_transacoes.append({
        "transaction_date": transacao.date,
        "value": float(transacao.amount),
        "description": transacao.memo
    })

# Cria o DataFrame
df = pd.DataFrame(dados_transacoes)

# Exibe as primeiras linhas da tabela
print(df.head())

df.to_clipboard()