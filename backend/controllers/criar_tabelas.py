# backend/controllers/criar_tabelas.py

from backend.utils.db import conectar

def criar_tabelas():
    conn = conectar()
    if conn is None:
        print("🚫 Sem conexão, abortando.")
        return

    cur = conn.cursor()
    cur.execute("""DROP TABLE IF EXISTS usuarios CASCADE;""")
    cur.execute("""
    CREATE TABLE usuarios (
      id SERIAL PRIMARY KEY,
      nome VARCHAR(100) NOT NULL,
      email VARCHAR(120) UNIQUE NOT NULL,
      senha TEXT NOT NULL,
      nacionalidade CHAR(2) NOT NULL,
      genero VARCHAR(20) NOT NULL,
      maior14 BOOLEAN NOT NULL DEFAULT TRUE
    );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabela usuarios recriada com sucesso.")

if __name__ == "__main__":
    criar_tabelas()
