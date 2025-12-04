#!/bin/bash
# Script to run the Flask web application

echo "Starting Unite Toolbox Flask App..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check for virtual environment
VENV_DIR="venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Check if Flask is installed in venv
if ! python -c "import flask" 2>/dev/null; then
    echo "Flask not found. Installing Flask and dependencies..."
    pip install --upgrade pip
    pip install flask
    # Install other requirements if they exist
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
fi

# Create necessary directories if they don't exist
mkdir -p uploads
mkdir -p results

# Copy Flask app and templates to main directory temporarily
# (Flask needs templates in a 'templates' folder relative to the app)
if [ ! -f "flask_app.py" ]; then
    cp archive/flask_app.py .
    cp -r archive/templates .
    FILES_COPIED=true
else
    FILES_COPIED=false
fi

echo ""
echo "Flask app will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Run Flask app
python flask_app.py

# Cleanup: remove copied files if we copied them
if [ "$FILES_COPIED" = true ]; then
    echo ""
    echo "Cleaning up temporary files..."
    rm flask_app.py
    rm -r templates
fi

# Deactivate virtual environment
deactivate

