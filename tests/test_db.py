def test_db_connection(db_conn):
    assert db_conn is not None, "Conexão deve ser estabelecida"

def test_table_exists(db_conn):
    cur = db_conn.cursor()
    cur.execute("""
        SELECT to_regclass('public.usuarios');
    """)
    result = cur.fetchone()[0]
    assert result == 'usuarios', "Tabela 'usuarios' deve existir"
    cur.close()
