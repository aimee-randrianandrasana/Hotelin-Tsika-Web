import psycopg2
import psycopg2.extras
from config import DATABASE_URL

_connection = None


def get_connection():
    global _connection
    if _connection is None:
        _connection = psycopg2.connect(DATABASE_URL)
        _connection.autocommit = True
    return _connection


def ensure_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(50), prenom VARCHAR(50), cin VARCHAR(20),
            tel VARCHAR(20), email VARCHAR(100),
            type_chambre VARCHAR(20) DEFAULT 'classic',
            chambre INT DEFAULT 1,
            date_debut DATE, date_fin DATE,
            prix_total INT DEFAULT 0
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients_archive (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(50), prenom VARCHAR(50), cin VARCHAR(20),
            tel VARCHAR(20), email VARCHAR(100),
            type_chambre VARCHAR(20) DEFAULT 'classic',
            chambre INT DEFAULT 1,
            date_debut DATE, date_fin DATE,
            prix_total INT DEFAULT 0,
            archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(50), prenom VARCHAR(50), cin VARCHAR(20),
            tel VARCHAR(20), poste VARCHAR(50),
            grade VARCHAR(20) DEFAULT 'Junior',
            salaire_base INT DEFAULT 0,
            absences INT DEFAULT 0,
            date_embauche DATE,
            last_paid TIMESTAMP DEFAULT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        );
    """)
    cur.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'employees' AND column_name = 'last_paid'
            ) THEN
                ALTER TABLE employees ADD COLUMN last_paid TIMESTAMP DEFAULT NULL;
            END IF;
        END $$;
    """)
    cur.close()
