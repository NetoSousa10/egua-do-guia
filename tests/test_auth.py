# tests/test_auth.py

import pytest

def test_cadastro_e_login(client):
    # Usuário de teste
    payload = {
        "nome":          "pytest_user",
        "email":         "pytest@example.com",
        "senha":         "senha123",
        "nacionalidade": "br",
        "genero":        "masculino",
        "maior14":       "on"
    }

    # 1) Cadastro — agora aceitamos 200, 201 (Created) ou 302 (redirect)
    res = client.post(
        "/auth/cadastro",
        json=payload,
        follow_redirects=True
    )
    assert res.status_code in (200, 201, 302), f"Esperava 200, 201 ou 302, mas veio {res.status_code}"

    # 2) Login
    login_payload = {
        "email": payload["email"],
        "senha": payload["senha"]
    }
    res = client.post(
        "/auth/login",
        json=login_payload,
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b"Login realizado com sucesso" in res.data
