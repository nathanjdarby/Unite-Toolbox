#!/bin/bash

# Unite Toolbox Launcher Script
echo "Starting Unite Toolbox..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Start the UniteToolbox executable
"$SCRIPT_DIR/UniteToolbox" &

# Wait for the Flask app to be fully loaded
echo "Waiting for Unite Toolbox to start..."
while ! curl -s http://localhost:5000 > /dev/null 2>&1; do
    sleep 1
done

echo "Unite Toolbox is ready! Opening browser..."

# Open the browser
open http://localhost:5000

echo "Unite Toolbox is running at http://localhost:5000"
echo "Press Ctrl+C to stop the application"

# Wait for the background process
wait 