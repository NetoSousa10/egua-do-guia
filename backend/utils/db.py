import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def conectar():
    try:
        conexao = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("✅ Conexão bem-sucedida ao banco de dados!")
        return conexao
    except Exception as e:
        print("❌ Erro ao conectar ao banco de dados:", e)
        return None
