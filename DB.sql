SET search_path TO public;

CREATE EXTENSION IF NOT EXISTS vector;

create table if not exists public.test_vectors(
	id serial primary key,
	embedding vector(3)
);


INSERT INTO public.test_vectors(embedding) VALUES
  ('[1,0,0]'),
  ('[0.9,0.1,0]'),
  ('[0,1,0]');

SELECT id, embedding, embedding <#> '[0.95,0.05,0]'::vector AS distance
FROM public.test_vectors
ORDER BY distance
LIMIT 10;



CREATE TABLE IF NOT EXISTS documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT,
  content TEXT,
  source TEXT,
  metadata JSONB,
  embedding VECTOR(1536),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Create HNSW index for fast similarity search
CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx
ON documents USING hnsw (embedding vector_cosine_ops);



DROP INDEX IF EXISTS documents_embedding_hnsw_idx;

ALTER TABLE documents
ALTER COLUMN embedding TYPE vector(384);

CREATE INDEX IF NOT EXISTS documents_embedding_hnsw_idx
ON documents
USING hnsw (embedding vector_cosine_ops);


SELECT COUNT(*) FROM documents;
select * from documents;





