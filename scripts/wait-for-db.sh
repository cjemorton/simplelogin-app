#!/bin/bash
# wait-for-db.sh - Wait for PostgreSQL to be ready
# Uses pg_isready by default, falls back to Python/psycopg2 if unavailable

set -e

# Default values
HOST="${DB_HOST:-localhost}"
PORT="${DB_PORT:-5432}"
USER="${DB_USER:-postgres}"
MAX_RETRIES="${DB_MAX_RETRIES:-30}"
RETRY_INTERVAL="${DB_RETRY_INTERVAL:-2}"

# Parse database connection string if DB_URI is set
if [ -n "$DB_URI" ]; then
    # Extract host, port, and user from DB_URI for pg_isready
    # Format: postgresql://user:password@host:port/database
    if [[ $DB_URI =~ postgresql://([^:]+):[^@]+@([^:]+):([^/]+)/ ]]; then
        USER="${BASH_REMATCH[1]}"
        HOST="${BASH_REMATCH[2]}"
        PORT="${BASH_REMATCH[3]}"
    elif [[ $DB_URI =~ postgresql://([^:]+):[^@]+@([^/]+)/ ]]; then
        USER="${BASH_REMATCH[1]}"
        HOST="${BASH_REMATCH[2]}"
        PORT="5432"
    fi
fi

echo "[INFO] Waiting for PostgreSQL at $HOST:$PORT (max retries: $MAX_RETRIES)..."

# Function to check database using pg_isready
check_with_pg_isready() {
    pg_isready -h "$HOST" -p "$PORT" -U "$USER" -q
    return $?
}

# Function to check database using Python/psycopg2
check_with_python() {
    # Export variables for Python to use securely
    export _DB_HOST="$HOST"
    export _DB_PORT="$PORT"
    export _DB_USER="$USER"
    export _DB_URI="$DB_URI"
    
    python3 -c '
import sys
import os
import psycopg2

try:
    # Try to use full DB_URI if available (includes password)
    db_uri = os.environ.get("_DB_URI", "")
    if db_uri:
        conn = psycopg2.connect(db_uri, connect_timeout=5)
    else:
        # Fallback to individual parameters (no password)
        conn = psycopg2.connect(
            host=os.environ["_DB_HOST"],
            port=os.environ["_DB_PORT"],
            user=os.environ["_DB_USER"],
            connect_timeout=5
        )
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
'
    return $?
}

# Determine which method to use
USE_PG_ISREADY=false
if command -v pg_isready &> /dev/null; then
    USE_PG_ISREADY=true
    echo "[INFO] Using pg_isready for database readiness checks"
else
    echo "[WARN] pg_isready not found, using Python/psycopg2 for database checks"
fi

# Wait for database to be ready
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if [ "$USE_PG_ISREADY" = true ]; then
        if check_with_pg_isready; then
            echo "[INFO] PostgreSQL is ready!"
            exit 0
        fi
    else
        if check_with_python; then
            echo "[INFO] PostgreSQL is ready!"
            exit 0
        fi
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        echo "[INFO] PostgreSQL not ready yet, waiting... (attempt $RETRY_COUNT/$MAX_RETRIES)"
        sleep $RETRY_INTERVAL
    fi
done

echo "[ERROR] PostgreSQL did not become ready after $MAX_RETRIES attempts"
exit 1
