# backend/controllers/criar_tabelas.py

import os
import sys

# Ajusta o PYTHONPATH para permitir imports de 'backend'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.utils.db import conectar
from backend.controllers.seed_places import seed_places

def criar_tabelas():
    conn = conectar()
    if conn is None:
        print("🚫 Sem conexão, abortando.")
        return

    cur = conn.cursor()

    # ——— Limpa tudo ———
    cur.execute("DROP TABLE IF EXISTS ratings CASCADE;")
    cur.execute("DROP TABLE IF EXISTS comments CASCADE;")
    cur.execute("DROP TABLE IF EXISTS user_favorites CASCADE;")
    cur.execute("DROP TABLE IF EXISTS followers CASCADE;")
    cur.execute("DROP TABLE IF EXISTS user_stats CASCADE;")
    cur.execute("DROP TABLE IF EXISTS places CASCADE;")
    cur.execute("DROP TABLE IF EXISTS usuarios CASCADE;")

    # ——— Usuários ———
    cur.execute("""
    CREATE TABLE usuarios (
      id            SERIAL PRIMARY KEY,
      nome          VARCHAR(100) NOT NULL,
      email         VARCHAR(120) UNIQUE NOT NULL,
      senha         TEXT NOT NULL,
      nacionalidade CHAR(2) NOT NULL,
      genero        VARCHAR(20) NOT NULL,
      maior14       BOOLEAN NOT NULL DEFAULT TRUE,
      criado_em     TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Lugares ———
    cur.execute("""
    CREATE TABLE places (
      id            SERIAL PRIMARY KEY,
      title         VARCHAR(150) NOT NULL UNIQUE,
      category      VARCHAR(30) NOT NULL,
      img_url       VARCHAR(255) NOT NULL,
      address       VARCHAR(255),
      phone         VARCHAR(50),
      price         VARCHAR(50),
      hours         VARCHAR(50),
      rating        SMALLINT,
      reviews       INT,
      features      TEXT[]       DEFAULT '{}',
      lat           NUMERIC(9,6) NOT NULL,
      lng           NUMERIC(9,6) NOT NULL
    );
    """)

    # ——— Estatísticas do usuário ———
    cur.execute("""
    CREATE TABLE user_stats (
      user_id      INT PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
      places_count INT DEFAULT 0,
      quiz_count   INT DEFAULT 0,
      total_xp     INT DEFAULT 0
    );
    """)

    # ——— Seguidores (self-join) ———
    cur.execute("""
    CREATE TABLE followers (
      follower_id  INT REFERENCES usuarios(id) ON DELETE CASCADE,
      followee_id  INT REFERENCES usuarios(id) ON DELETE CASCADE,
      seguido_em   TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
      PRIMARY KEY (follower_id, followee_id)
    );
    """)

    # ——— Favoritos / visitas ———
    cur.execute("""
    CREATE TABLE user_favorites (
      user_id      INT REFERENCES usuarios(id) ON DELETE CASCADE,
      place_id     INT REFERENCES places(id) ON DELETE CASCADE,
      visits       INT DEFAULT 0,
      PRIMARY KEY (user_id, place_id)
    );
    """)

    # ——— Comentários ———
    cur.execute("""
    CREATE TABLE comments (
      id            SERIAL PRIMARY KEY,
      user_id       INT REFERENCES usuarios(id) ON DELETE CASCADE,
      place_id      INT REFERENCES places(id) ON DELETE CASCADE,
      content       TEXT NOT NULL,
      criado_em     TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Avaliações ———
    cur.execute("""
    CREATE TABLE ratings (
      user_id       INT REFERENCES usuarios(id) ON DELETE CASCADE,
      place_id      INT REFERENCES places(id) ON DELETE CASCADE,
      score         SMALLINT CHECK (score BETWEEN 1 AND 5),
      PRIMARY KEY (user_id, place_id)
    );
    """)

    # ——— View de perfil de usuário ———
    cur.execute("""
    CREATE OR REPLACE VIEW user_profile AS
    SELECT
      u.id,
      u.nome,
      u.email,
      us.places_count,
      us.quiz_count,
      us.total_xp,
      COALESCE(c.comment_count, 0)   AS comments_count,
      COALESCE(f.followers_count, 0)  AS followers_count,
      COALESCE(fw.following_count, 0) AS following_count
    FROM usuarios u
    LEFT JOIN user_stats us     ON us.user_id = u.id
    LEFT JOIN (
      SELECT user_id, COUNT(*) AS comment_count
      FROM comments GROUP BY user_id
    ) c  ON c.user_id = u.id
    LEFT JOIN (
      SELECT followee_id, COUNT(*) AS followers_count
      FROM followers GROUP BY followee_id
    ) f  ON f.followee_id = u.id
    LEFT JOIN (
      SELECT follower_id, COUNT(*) AS following_count
      FROM followers GROUP BY follower_id
    ) fw ON fw.follower_id = u.id;
    """)

    # ——— Trigger para favoritos ———
    cur.execute("""
    CREATE OR REPLACE FUNCTION trg_inc_places_count()
    RETURNS TRIGGER AS $$
    BEGIN
      UPDATE user_stats
        SET places_count = places_count + 1
      WHERE user_id = NEW.user_id;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    cur.execute("DROP TRIGGER IF EXISTS after_fav_insert ON user_favorites;")
    cur.execute("""
    CREATE TRIGGER after_fav_insert
      AFTER INSERT ON user_favorites
      FOR EACH ROW
      EXECUTE PROCEDURE trg_inc_places_count();
    """)

    # ——— Aplica e fecha ———
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabelas, view e trigger criados com sucesso.")

if __name__ == "__main__":
    # 1) Cria tabelas, view e trigger
    criar_tabelas()
    # 2) Semeia os places via seu seed_places.py
    seed_places()
