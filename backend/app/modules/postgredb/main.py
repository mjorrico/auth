import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

# Define DB config once
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "backend")
DB_NAME = os.getenv("POSTGRES_DB", "auth")
print(f"Checking database {DB_NAME} at {DB_HOST}:{DB_PORT} as {DB_USER}...")

try:
    # Connect to the default 'postgres' database to manage databases
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    with conn.cursor() as cur:
        # Check if database exists
        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,)
        )
        exists = cur.fetchone()
        if not exists:
            print(f"Creating database {DB_NAME}...")
            cur.execute(f'CREATE DATABASE "{DB_NAME}"')
        else:
            print(f"Database {DB_NAME} already exists.")

    conn.close()
except Exception as e:
    print(f"Warning: Could not check/create database: {e}")


class PostgresClient:
    def __init__(self):
        # Instantiate ONCE for the whole app
        self.connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            cursor_factory=RealDictCursor,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

    @contextmanager
    def transaction(self):
        """Managed cursor: Auto-borrows, Auto-commits, Auto-returns to pool."""
        conn = self.connection_pool.getconn()
        try:
            conn.autocommit = False
            with conn.cursor() as cur:
                yield cur  # Your logic runs here
            conn.commit()  # Success!
        except Exception as e:
            conn.rollback()  # Failure!
            raise e
        finally:
            # Always return connection to the pool, even on crash
            self.connection_pool.putconn(conn)

    def close(self):
        self.connection_pool.closeall()


# --- Usage ---
db = PostgresClient()  # Do this once at the top level


# In your API route:
def create_user(name):
    with db.transaction() as cur:
        cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    # No .commit() needed! It's already done.
