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
    is_verified BOOLEAN DEFAULT false NOT NULL,
    is_banned BOOLEAN DEFAULT false NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (email, password_hash, is_verified, is_banned)
VALUES 
    -- 1. Verified User
    (
        'verified@jordanenrico.com', 
        '$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU', 
        true, 
        false
    ),
    -- 2. Unverified & Unbanned User
    (
        'unverified@jordanenrico.com', 
        '$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU', 
        false, 
        false
    ),
    -- 3. Banned User
    (
        'banned@jordanenrico.com', 
        '$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU', 
        true, 
        true
    );
