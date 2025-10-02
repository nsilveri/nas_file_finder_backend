-- Tabella per le cartelle
CREATE TABLE IF NOT EXISTS folders (
    id SERIAL PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    last_modified TIMESTAMP NOT NULL
);

-- Tabella per i file
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    directory TEXT NOT NULL,
    last_modified TIMESTAMP NOT NULL,
    UNIQUE(filename, directory)
);
