-- Create database
CREATE DATABASE onlinestore;

\connect onlinestore;

-- Load schema
\i /docker-entrypoint-initdb.d/01_schema.sql
\i /docker-entrypoint-initdb.d/02_triggers.sql
\i /docker-entrypoint-initdb.d/03_indexes.sql
