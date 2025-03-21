#!/bin/bash

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "Running in $KITE_DB_MODE mode with DB: $DATABASE_URL"

# Start the application
python main.py
