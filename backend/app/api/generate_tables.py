import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

from app.modules.postgredb import PostgresClient
from app.modules.auth_tools.template_data import (
    TEMPLATE_USERS,
    TEMPLATE_CAPABILITIES,
    TEMPLATE_ROLES,
    TEMPLATE_ROLE_CAPABILITIES,
    TEMPLATE_MENUS,
)

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
DB_NAME = os.getenv("POSTGRES_DB", "auth")


def ensure_database_exists():
    """Connects to the postgres maintenance DB and creates DB_NAME if it doesn't exist.

    CREATE DATABASE cannot run inside a transaction block, so this uses
    ISOLATION_LEVEL_AUTOCOMMIT on a dedicated connection to the 'postgres' DB.
    """
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                (DB_NAME,),
            )
            if cur.fetchone() is None:
                print(f"Database '{DB_NAME}' not found — creating it...")
                cur.execute(f'CREATE DATABASE "{DB_NAME}"')
            else:
                print(f"Database '{DB_NAME}' already exists, skipping creation.")
    finally:
        conn.close()


def initialize_schema_and_data():
    """Enables extensions, creates tables, and inserts initial data in a single flow."""
    print("Initialising database schema and data...")

    ensure_database_exists()
    db = PostgresClient()

    with db.transaction() as cur:
        # Enable vector extension
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        # Create documents table and index
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(1024)
            );
            CREATE INDEX IF NOT EXISTS documents_embedding_idx ON documents 
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
        """
        )

        # Create menus table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS menus (
                id UUID PRIMARY KEY NOT NULL,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
        """
        )

        # Create capabilities table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS capabilities (
                id UUID PRIMARY KEY NOT NULL,
                menu_id UUID,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                FOREIGN KEY (menu_id) REFERENCES menus(id)
            );
        """
        )

        # Create roles table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id UUID PRIMARY KEY NOT NULL,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            );
        """
        )

        # Create role_capabilities table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS role_capabilities (
                role_id UUID NOT NULL,
                capability_id UUID NOT NULL,
                PRIMARY KEY (role_id, capability_id),
                FOREIGN KEY (role_id) REFERENCES roles(id),
                FOREIGN KEY (capability_id) REFERENCES capabilities(id)
            );
        """
        )

        # Create users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_verified BOOLEAN DEFAULT false NOT NULL,
                is_banned BOOLEAN DEFAULT false NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                role UUID NOT NULL,
                FOREIGN KEY (role) REFERENCES roles(id)
            );
        """
        )

        # insert menus
        print("Inserting initial menus...")
        cur.executemany(
            """
            INSERT INTO menus (id, name, description)
            VALUES (%s, %s, %s);
            """,
            TEMPLATE_MENUS,
        )

        # Insert initial roles
        print("Inserting initial roles...")
        cur.executemany(
            """
            INSERT INTO roles (id, name, description)
            VALUES (%s, %s, %s)
            """,
            TEMPLATE_ROLES,
        )

        # Insert initial users
        print("Inserting initial users...")
        cur.executemany(
            """
            INSERT INTO users (email, password_hash, is_verified, is_banned, role)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
            """,
            TEMPLATE_USERS,
        )

        # Insert initial capabilities
        print("Inserting initial capabilities...")
        cur.executemany(
            """
            INSERT INTO capabilities (id, name, description, menu_id)
            VALUES (%s, %s, %s, %s);
            """,
            TEMPLATE_CAPABILITIES,
        )

        # Insert initial role_capabilities
        print("Inserting initial role_capabilities...")
        cur.executemany(
            """
            INSERT INTO role_capabilities (role_id, capability_id)
            VALUES (%s, %s);
            """,
            TEMPLATE_ROLE_CAPABILITIES,
        )


if __name__ == "__main__":
    try:
        initialize_schema_and_data()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
