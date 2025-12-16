DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'sa') THEN
    CREATE ROLE sa WITH LOGIN PASSWORD 'YourStrong!Passw0rd';
  END IF;

  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'project') THEN
    CREATE DATABASE project OWNER sa;
  END IF;

  -- на случай, если БД уже есть, но владелец другой:
  ALTER DATABASE project OWNER TO sa;

  GRANT ALL PRIVILEGES ON DATABASE project TO sa;
END
$$;
