import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()


class PostgresClient:
    def __init__(self):
        # Instantiate ONCE for the whole app
        self.connection_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("POSTGRES_HOST", "localhost"),
            dbname=os.getenv("POSTGRES_DB", "postgres"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "backend"),
            cursor_factory=RealDictCursor,
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
