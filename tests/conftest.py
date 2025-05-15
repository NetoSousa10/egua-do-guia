# tests/conftest.py

import os
import sys
import pytest

# Garante que o diretório raiz do projeto fique no PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.app import create_app
from backend.controllers.criar_tabelas import criar_tabelas
from backend.utils.db import conectar

@pytest.fixture(scope="session")
def app():
    # usa um banco de testes isolado
    os.environ["DATABASE_URL"] = "postgresql://postgres:xablau@localhost:5432/egua_do_guia"
    app = create_app()
    app.config.update(TESTING=True)
    # (re)cria o esquema de teste
    criar_tabelas()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def db_cleanup():
    # limpa a tabela antes de cada teste
    conn = conectar()
    cur = conn.cursor()
    cur.execute("TRUNCATE usuarios RESTART IDENTITY CASCADE")
    conn.commit()
    cur.close()
    conn.close()
