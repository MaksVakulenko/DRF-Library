-- Check if the 'admin' role exists; if not, create it
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
        CREATE ROLE admin WITH LOGIN PASSWORD 'some_password';
    END IF;
END $$;

-- Check if the 'library_db' database exists; if not, create it
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'library_db') THEN
        CREATE DATABASE library_db;
    END IF;
END $$;

-- Change the database owner to 'admin'
ALTER DATABASE library_db OWNER TO admin;

-- Connect to 'library_db'
\c library_db

-- Grant full privileges on all existing tables in the 'public' schema to 'admin'
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;

-- Ensure 'admin' has privileges on all future tables created in the 'public' schema
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;