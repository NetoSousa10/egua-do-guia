# backend/utils/db.py
import os
import psycopg2
from dotenv import load_dotenv

# Carrega o .env (agora que o path não tem acentos, o default UTF-8 já resolve)
load_dotenv()

def conectar():
    url = os.getenv("DATABASE_URL")
    if not url:
        print("❌ DATABASE_URL não configurada.")
        return None

    print("🔍 Tentando conectar a:", url)
    try:
        conexao = psycopg2.connect(url)
        print("✅ Conexão ok!")
        return conexao
    except Exception as e:
        print("❌ Erro ao conectar:", e)
        return None
