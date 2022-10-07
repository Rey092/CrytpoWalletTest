CREATE USER test_user WITH PASSWORD 'test_password';

CREATE DATABASE test_database_db;
GRANT ALL PRIVILEGES ON DATABASE test_database_db TO test_user;
