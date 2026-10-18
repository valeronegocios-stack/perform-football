-- Perform Football: esquema v0.3 (una cuenta, estado sincronizado)
-- Se crea automáticamente al arrancar el servidor con DATABASE_URL.
CREATE TABLE IF NOT EXISTS pf_state (
  account_key TEXT PRIMARY KEY CHECK (account_key='principal'),
  revision BIGINT NOT NULL DEFAULT 0 CHECK (revision>=0),
  snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
-- v0.3 guarda profile, sessions, checkins, meals y chat en el snapshot JSONB.
-- Futuras versiones migrarán entidades a tablas propias si hacen falta.
