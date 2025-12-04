#!/bin/bash
# Build script for Unite Toolbox Flask Web Application executable
# Creates a universal binary for both Intel and Apple Silicon Macs

echo "Building Unite Toolbox Flask Web App executable (Universal Binary)..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Check Python architecture
PYTHON_ARCH=$(python3 -c "import platform; print(platform.machine())")
echo "Current Python architecture: $PYTHON_ARCH"

# Check if Python is Universal2
if [[ "$PYTHON_ARCH" != "arm64" && "$PYTHON_ARCH" != "x86_64" ]]; then
    echo "Warning: Python may not be Universal2. Universal binary build may fail."
    echo "For best results, use a Universal2 Python installation from python.org"
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/

# Create necessary directories
mkdir -p uploads
mkdir -p results

# Build the executable for current architecture
echo "Building executable from flask_app.spec..."
echo ""
echo "Building for Apple Silicon (arm64) architecture..."
echo "This build will work on:"
echo "  ✓ Apple Silicon Macs (native - fastest)"
echo "  ✓ Intel Macs (via Rosetta 2 - works great)"
echo ""
pyinstaller flask_app.spec

# Check if build was successful
if [ -d "dist/UniteToolboxWeb.app" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "✓ Executable created at: dist/UniteToolboxWeb.app"
    echo ""
    echo "To run the app, double-click UniteToolboxWeb.app or run:"
    echo "  open dist/UniteToolboxWeb.app"
    echo ""
    echo "The app will automatically:"
    echo "  - Start the Flask web server"
    echo "  - Open your browser to http://127.0.0.1:5000"
else
    echo ""
    echo "✗ Build failed. Check the output above for errors."
    exit 1
fi

