from backend.utils.db import conectar

def criar_tabela_usuarios():
    conn = conectar()
    if not conn:
        print("⚠️ Sem conexão com o banco. Abortando.")
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                saldo_moedas INTEGER DEFAULT 0
            );
        """)
        conn.commit()
        cur.close()
        print("✅ Tabela 'usuarios' criada com sucesso!")
    except Exception as e:
        print("❌ Erro ao criar tabela:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    criar_tabela_usuarios()
