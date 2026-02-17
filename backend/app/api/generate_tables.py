import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

from app.modules.postgredb import PostgresClient

load_dotenv()


def initialize_schema_and_data():
    """Enables extensions, creates tables, and inserts initial data in a single flow."""
    print("Initialising database schema and data...")

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

        # Create users table
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_verified BOOLEAN DEFAULT false NOT NULL,
                is_banned BOOLEAN DEFAULT false NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """
        )

        # Insert initial data
        print("Inserting initial users...")
        users_data = [
            (
                "verified@jordanenrico.com",
                "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
                True,
                False,
            ),
            (
                "unverified@jordanenrico.com",
                "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
                False,
                False,
            ),
            (
                "banned@jordanenrico.com",
                "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
                True,
                True,
            ),
        ]

        for user_row in users_data:
            cur.execute(
                """
                INSERT INTO users (email, password_hash, is_verified, is_banned)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """,
                user_row,
            )


if __name__ == "__main__":
    try:
        initialize_schema_and_data()
        print("Database initialization complete.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
