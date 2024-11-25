SELECT 'CREATE DATABASE ufcdb'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ufcdb')\gexec