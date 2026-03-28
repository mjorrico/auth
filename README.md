# Authy

A JWT-based authentication backend built with **FastAPI** and **PostgreSQL** (via pgvector).

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- The **pgvector** service running in Docker (see below)

---

## Environment setup

Copy and fill in the env file for the backend:

```bash
cp backend/.env.example backend/.env
```

Key variables in `backend/.env`:

| Variable            | Description                          | Example          |
|---------------------|--------------------------------------|------------------|
| `POSTGRES_HOST`     | Hostname of the pgvector container   | `pgvector`       |
| `POSTGRES_PORT`     | Port PostgreSQL listens on           | `5432`           |
| `POSTGRES_USER`     | Database user                        | `postgres`       |
| `POSTGRES_PASSWORD` | Database password                    | `yourpassword`   |
| `POSTGRES_DB`       | Target database name                 | `auth`           |
| `JWT_SECRET`        | Secret key for signing JWT tokens    | `<random string>`|
| `JWT_ALGORITHM`     | JWT signing algorithm                | `HS256`          |

> **Note:** `POSTGRES_HOST` should be the container name of the pgvector service (`pgvector`), not `localhost`, when running inside Docker.

---

## Spin-up order

### Step 1 — Start the pgvector service (external project)

The database lives in a separate compose project. Start it first:

```bash
# From the directory containing your pgvector compose file
docker compose up -d
```

Verify it's running and on `pgvector_network`:

```bash
docker network inspect pgvector_network
```

You should see the `pgvector` container listed under `Containers`.

---

### Step 2 — Build and start the backend

From the root of **this** repository:

```bash
docker compose up -d --build
```

This will:
- Build the `backend` image from `backend/Dockerfile`
- Attach the container to the external `pgvector_network` so it can reach `pgvector`
- Expose the API on **http://localhost:8000**

---

### Step 3 — Initialise the database schema and seed data

Run `generate_tables.py` inside the running backend container. It will:
1. Create the target database if it doesn't already exist
2. Enable the `vector` extension
3. Create the `documents` and `users` tables (idempotent — safe to re-run)
4. Insert seed users (skipped if they already exist via `ON CONFLICT DO NOTHING`)

```bash
docker exec -it auth-backend-1 python -m app.api.generate_tables
```

> **Tip:** If you're unsure of the container name, check with `docker ps` and look for the backend container. Alternatively, set `container_name: backend` in `compose.yaml` and use that name directly.

Expected output:

```
Initialising database schema and data...
Database 'auth' already exists, skipping creation.
Inserting initial users...
Database initialization complete.
```

---

## API

Once running, the interactive docs are available at:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc
- **Health check** → http://localhost:8000/api/v1/health

---

## Teardown

```bash
# Stop and remove the backend container
docker compose down

# Stop pgvector (from its own project directory)
docker compose down
```
