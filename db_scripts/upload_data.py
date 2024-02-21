#!/usr/bin/env python3

import glob

import psycopg
from fire import Fire
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

conn = psycopg.connect(
    dbname="db1",
    autocommit=True,
    user="admin",
    password="password",
    host="db",
    port=5432,
)

conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)

model = SentenceTransformer("all-MiniLM-L6-v2").cuda()


def main(directory: str):
    conn.execute("DROP TABLE IF EXISTS documents")
    conn.execute(
        "CREATE TABLE documents (id bigserial PRIMARY KEY, content text, embedding vector(384))"
    )
    articles = glob.glob(f"{directory}/*.txt")
    input = list(map(lambda article: open(article, "r").read(), articles))
    embeddings = model.encode(input)

    for content, embedding in zip(input, embeddings):
        conn.execute(
            "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
            (content, embedding),
        )


def get_nearest_neighbor(query: str):
    embedding = model.encode([query])[0]
    result = conn.execute(
        "SELECT content, embedding <-> %s AS distance FROM documents ORDER BY distance LIMIT 1",
        (embedding,),
    )
    text = list(result)[0][0]
    return text


if __name__ == "__main__":
    Fire(main)
