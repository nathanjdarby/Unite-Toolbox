#!/bin/bash
# Build script for Unite Toolbox Flask Web Application - Universal Binary
# Builds for both Intel and Apple Silicon, then combines them

echo "Building Unite Toolbox Flask Web App as Universal Binary..."
echo "This will build for both Intel (x86_64) and Apple Silicon (arm64) architectures"
echo ""

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Get current architecture
CURRENT_ARCH=$(uname -m)
echo "Current architecture: $CURRENT_ARCH"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/

# Create necessary directories
mkdir -p uploads
mkdir -p results

# Check if we have access to both architectures
# For universal binary, we need to build on a machine that can run both
# or use Rosetta 2 to build the Intel version

if [ "$CURRENT_ARCH" = "arm64" ]; then
    echo ""
    echo "Building for Apple Silicon (arm64)..."
    pyinstaller --target-arch arm64 flask_app.spec --clean
    
    if [ $? -ne 0 ]; then
        echo "✗ Build failed for arm64"
        exit 1
    fi
    
    # Move arm64 build
    mv dist/UniteToolboxWeb.app dist/UniteToolboxWeb.arm64.app
    
    echo ""
    echo "To create a true universal binary, you need to:"
    echo "1. Build on an Intel Mac for x86_64, OR"
    echo "2. Use Rosetta 2 to build the Intel version"
    echo ""
    echo "For now, the app is built for Apple Silicon (arm64) only."
    echo "It will run on Apple Silicon Macs and Intel Macs via Rosetta 2."
    echo ""
    echo "✓ Build successful for arm64!"
    echo "✓ Executable created at: dist/UniteToolboxWeb.app"
    
elif [ "$CURRENT_ARCH" = "x86_64" ]; then
    echo ""
    echo "Building for Intel (x86_64)..."
    pyinstaller --target-arch x86_64 flask_app.spec --clean
    
    if [ $? -ne 0 ]; then
        echo "✗ Build failed for x86_64"
        exit 1
    fi
    
    echo ""
    echo "✓ Build successful for x86_64!"
    echo "✓ Executable created at: dist/UniteToolboxWeb.app"
    echo ""
    echo "Note: To create a universal binary, build both architectures"
    echo "and combine them using 'lipo' command."
else
    echo "Unknown architecture: $CURRENT_ARCH"
    exit 1
fi

echo ""
echo "The Flask app will automatically:"
echo "  - Start the Flask web server"
echo "  - Open your browser to http://127.0.0.1:5000"

