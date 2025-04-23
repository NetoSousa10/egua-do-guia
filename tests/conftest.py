# tests/conftest.py
import os
import sys
import pytest

# Garante que a raiz do projeto (onde fica 'backend/') esteja no path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.utils.db import conectar
from backend.app import create_app  # ou 'from run import create_app', se seu entrypoint for run.py

@pytest.fixture(scope="session")
def app():
    # (Opcional) força usar o mesmo banco de testes
    os.environ['DATABASE_URL'] = "postgresql://postgres:xablau@localhost:5432/egua_do_guia"
    
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG":   False,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="session")
def db_conn():
    conn = conectar()
    yield conn
    conn.close()
