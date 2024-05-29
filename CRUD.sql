-- Create, Insert and Read
CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

-- L2 Distance 
SELECT embedding <-> '[3,1,2]' AS distance FROM items;

-- Average Vector
SELECT AVG(embedding) FROM items;

-- Update and Read
UPDATE items SET embedding = '[3,2,1]' WHERE id = 1;
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

-- Delete and Read
DELETE FROM items WHERE id = 1;
SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;

DELETE FROM items;
SELECT * FROM items;

DROP TABLE items;


DELETE FROM documents;