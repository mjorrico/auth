CREATE DATABASE auth;

\c auth

CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1024)
);
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuidv7(), 
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (email, password_hash)
VALUES (
    'guest@jordanenrico.com',
    '$argon2id$v=19$m=65536,t=3,p=4$j0CMd+3jf5XVNOaiaSbzxQ$Z4ToXqQYKO3BuiqIhqX8Sc0RHJaTwgZBM6QtsdLp9Kg'
);
