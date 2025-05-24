# backend/controllers/criar_tabelas.py

import os
import sys

# Ajusta o PYTHONPATH para permitir imports de 'backend'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.utils.db import conectar
from backend.controllers.seed_places import seed_places

def seed_store_items():
    conn = conectar()
    cur = conn.cursor()
    # limpa antes de inserir, assim não duplica em re-runs
    cur.execute("""
      TRUNCATE TABLE store_items, user_items RESTART IDENTITY CASCADE;""")


    items = [
        ('roupas',  'Paysandu',      30, '/static/assets/img/roupas1.png'),
        ('roupas',  'Remo',          30, '/static/assets/img/roupas2.png'),
        ('roupas',  'Brasil',        40, '/static/assets/img/roupas3.png'),
        ('avatar',  'Sorridente',    30, '/static/assets/img/avatar1.png'),
        ('avatar',  'Feliz!',        40, '/static/assets/img/avatar2.png'),
        ('avatar',  'Grito!',        50, '/static/assets/img/avatar3.png'),
        ('cupons',  '15% Desconto',  30, '/static/assets/img/cupom1.png'),
        ('cupons',  '20% Desconto',  40, '/static/assets/img/cupom2.png'),
        ('cupons',  '5% Desconto',   20, '/static/assets/img/cupom3.png'),
        ('cupons',  'Bebida Grátis', 50, '/static/assets/img/cupom4.png'),
        ('temas',   'Tema 1',        20, '/static/assets/img/tema1.png'),
        ('temas',   'Tema 2',        20, '/static/assets/img/tema2.png'),
        ('temas',   'Tema 3',        20, '/static/assets/img/tema3.png'),
    ]

    cur.executemany(
        "INSERT INTO store_items (category, name, price, img_url) VALUES (%s, %s, %s, %s);",
        items
    )
    conn.commit()
    cur.close()
    conn.close()

def criar_tabelas():
    conn = conectar()
    if conn is None:
        print("🚫 Sem conexão, abortando.")
        return

    cur = conn.cursor()

    # ——— Limpa tudo ———
    cur.execute("DROP VIEW IF EXISTS user_profile CASCADE;")
    cur.execute("DROP VIEW IF EXISTS places_with_stats CASCADE;")
    cur.execute("DROP TABLE IF EXISTS ratings CASCADE;")
    cur.execute("DROP TABLE IF EXISTS comments CASCADE;")
    cur.execute("DROP TABLE IF EXISTS user_favorites CASCADE;")
    cur.execute("DROP TABLE IF EXISTS user_stats CASCADE;")
    cur.execute("DROP TABLE IF EXISTS quiz_results CASCADE;")
    cur.execute("DROP TABLE IF EXISTS visits CASCADE;")
    cur.execute("DROP TABLE IF EXISTS user_ranks CASCADE;")
    cur.execute("DROP TABLE IF EXISTS places CASCADE;")
    cur.execute("DROP TABLE IF EXISTS usuarios CASCADE;")

    # ——— Usuários ———
    cur.execute("""
    CREATE TABLE usuarios (
      id            SERIAL PRIMARY KEY,
      nome          VARCHAR(100) NOT NULL,
      email         VARCHAR(120) UNIQUE NOT NULL,
      senha         TEXT NOT NULL,
      nacionalidade CHAR(2)     NOT NULL,
      genero        VARCHAR(20)  NOT NULL,
      maior14       BOOLEAN      NOT NULL DEFAULT TRUE,
      avatar_url    VARCHAR(255),
      tutorial_done BOOLEAN      NOT NULL DEFAULT FALSE,
      coins         INT          NOT NULL DEFAULT 0,
      criado_em     TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Lugares ———
    cur.execute("""
    CREATE TABLE places (
      id            SERIAL PRIMARY KEY,
      title         VARCHAR(150) NOT NULL UNIQUE,
      category      VARCHAR(30)  NOT NULL,
      img_url       VARCHAR(255) NOT NULL,
      address       VARCHAR(255),
      phone         VARCHAR(50),
      price         VARCHAR(50),
      hours         VARCHAR(50),
      features      TEXT[]        DEFAULT '{}',
      lat           NUMERIC(9,6)  NOT NULL,
      lng           NUMERIC(9,6)  NOT NULL
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

    # ——— Resultados de quiz ———
    cur.execute("""
    CREATE TABLE quiz_results (
      id       SERIAL PRIMARY KEY,
      user_id  INT REFERENCES usuarios(id) ON DELETE CASCADE,
      xp       INT NOT NULL,
      feito_em TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Histórico de visitas ———
    cur.execute("""
    CREATE TABLE visits (
      user_id    INT REFERENCES usuarios(id) ON DELETE CASCADE,
      place_id   INT REFERENCES places(id) ON DELETE CASCADE,
      visited_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
      PRIMARY KEY (user_id, place_id, visited_at)
    );
    """)

    # ——— Favoritos ———
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

    # ——— Ranks de usuário ———
    cur.execute("""
    CREATE TABLE user_ranks (
      user_id   INT PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
      rank_name VARCHAR(50) NOT NULL
    );
    """)

    # ——— View agregada de places (com média e total de reviews) ———
    cur.execute("""
    CREATE OR REPLACE VIEW places_with_stats AS
    SELECT
      p.id,
      p.title,
      p.category,
      p.img_url       AS imgUrl,
      p.address,
      p.phone,
      p.price,
      p.hours,
      COALESCE(ROUND(AVG(r.score))::INT, 0) AS rating,
      COUNT(r.*)                        AS reviews,
      p.features,
      p.lat,
      p.lng
    FROM places p
    LEFT JOIN ratings r ON r.place_id = p.id
    GROUP BY p.id;
    """)

    # ——— View de perfil de usuário ———
    cur.execute("""
    CREATE OR REPLACE VIEW user_profile AS
    SELECT
      u.id,
      u.nome           AS name,
      u.avatar_url     AS avatar,
      us.places_count,
      us.quiz_count,
      us.total_xp,
      COALESCE(c.comment_count, 0)    AS comments_count,
      COALESCE(v.visits_count, 0)     AS places_visited,
      COALESCE(rfav.visits, 0)        AS favorite_place_visits,
      fp.title        AS favorite_place,
      fp.img_url      AS favorite_place_img,
      COALESCE(rr.avg_rating, 0)      AS favorite_place_rating,
      CASE
        WHEN us.total_xp >= 300 THEN 'Ouro'
        WHEN us.total_xp >= 100 THEN 'Prata'
        ELSE 'Bronze'
      END AS rank
    FROM usuarios u
    LEFT JOIN user_stats us     ON us.user_id = u.id
    LEFT JOIN (
      SELECT user_id, COUNT(*) AS comment_count
      FROM comments GROUP BY user_id
    ) c ON c.user_id = u.id
    LEFT JOIN (
      SELECT user_id, COUNT(*) AS visits_count
      FROM visits GROUP BY user_id
    ) v ON v.user_id = u.id
    LEFT JOIN LATERAL (
      SELECT uf.place_id, uf.visits
      FROM user_favorites uf
      WHERE uf.user_id = u.id
      ORDER BY uf.visits DESC
      LIMIT 1
    ) rfav ON TRUE
    LEFT JOIN places fp ON fp.id = rfav.place_id
    LEFT JOIN LATERAL (
      SELECT ROUND(AVG(r.score)::numeric,1) AS avg_rating
      FROM ratings r
      WHERE r.place_id = rfav.place_id
    ) rr ON TRUE;
    """)

    # ——— Trigger para incrementar places_count em user_stats ———
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

    # ——— Loja: tabela de itens e posse ———
    cur.execute("""
    CREATE TABLE IF NOT EXISTS store_items (
      id       SERIAL PRIMARY KEY,
      category VARCHAR(50) NOT NULL,
      name     TEXT       NOT NULL,
      price    INT        NOT NULL,
      img_url  TEXT       NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_items (
      id          SERIAL PRIMARY KEY,
      user_id     INT REFERENCES usuarios(id) ON DELETE CASCADE,
      item_id     INT REFERENCES store_items(id) ON DELETE CASCADE,
      equipped    BOOLEAN NOT NULL DEFAULT FALSE,
      acquired_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Tabela para status do tutorial ———
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_tutorial (
      user_id    INT PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
      completed  BOOLEAN NOT NULL DEFAULT FALSE,
      skipped    BOOLEAN NOT NULL DEFAULT FALSE,
      updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
    );
    """)

    # ——— Trigger para premiar 20 coins na conclusão do tutorial ———
    cur.execute("""
    CREATE OR REPLACE FUNCTION trg_reward_tutorial()
    RETURNS TRIGGER AS $$
    BEGIN
      IF TG_OP = 'UPDATE'
         AND NEW.completed = TRUE
         AND (OLD.completed = FALSE OR OLD.completed IS NULL) THEN
        UPDATE usuarios
          SET coins = coins + 20
        WHERE id = NEW.user_id;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """)
    cur.execute("DROP TRIGGER IF EXISTS after_tutorial_update ON user_tutorial;")
    cur.execute("""
    CREATE TRIGGER after_tutorial_update
      AFTER UPDATE ON user_tutorial
      FOR EACH ROW
      EXECUTE PROCEDURE trg_reward_tutorial();
    """)

    # ——— Finaliza e fecha conexão ———
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabelas, views e triggers criados com sucesso.")

if __name__ == "__main__":
    criar_tabelas()
    seed_places()
    seed_store_items()
    print("👍 Dados iniciais de lugares e loja inseridos com sucesso!")
