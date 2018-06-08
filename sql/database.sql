CREATE DATABASE openroad;

CREATE USER openroad_user WITH PASSWORD 'openroad';

ALTER ROLE openroad_user SET client_encoding TO 'utf8';
ALTER ROLE openroad_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE openroad TO openroad_user;