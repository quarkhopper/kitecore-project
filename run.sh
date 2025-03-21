#!/bin/bash

# Function to get the script's directory
get_script_dir() {
    SOURCE="${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do
        DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
        SOURCE="$(readlink "$SOURCE")"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
    done
    DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
    echo "$DIR"
}

# Change to the script's directory only if not sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    cd "$(get_script_dir)" || exit 1
fi

# Load environment variables
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

echo "Running in $KITE_DB_MODE mode with DB: $DATABASE_URL"

# Activate the virtual environment
source venv/Scripts/activate

# Start the application
python main.py
