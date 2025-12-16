#!/usr/bin/env sh
set -e

# Optional: autogeneration (only in DEV)
if [ "${ALEMBIC_AUTOGEN:-0}" = "1" ]; then
  echo "[migrate] Autogenerate enabled"
  # We'll be gentle: if there are no changes, we'll just let you know
  set +e
  OUT="$(alembic revision --autogenerate -m "autogen $(date -Iseconds)")"
  CODE=$?
  set -e
  echo "$OUT"
  echo "$OUT" | grep -q "No changes in schema detected." && \
    echo "[migrate] No schema changes, skipping autogen." || \
    echo "[migrate] New revision generated."
fi

# Always use migrations
echo "[migrate] Upgrading to head…"
alembic upgrade head
echo "[migrate] Done."
