#!/bin/sh

echo "Running entrypoint.sh..."

# Check if SERVICE environment variable is set
if [ -z "$SERVICE" ]; then
  echo "SERVICE environment variable is not set"
  exit 1
fi

# Run the corresponding command based on the value of SERVICE
if [ "$SERVICE" = "migrations" ]; then
    echo "Triggering migrations..."
    alembic upgrade head
elif [ "$SERVICE" = "api" ]; then
    echo "Triggering claims api..."
    python entrypoint_api.py
else
    echo "Unknown SERVICE: $SERVICE"
    exit 1
fi
