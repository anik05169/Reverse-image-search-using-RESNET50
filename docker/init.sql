-- docker/init.sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    filename TEXT,
    category TEXT,
    embedding vector(2048) -- ResNet50 output size
);

-- Create the HNSW index for speed
CREATE INDEX ON inventory USING hnsw (embedding vector_cosine_ops);