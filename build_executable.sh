#!/bin/bash
# Build script for Unite Toolbox executable
# Creates a universal binary for both Intel and Apple Silicon Macs

echo "Building Unite Toolbox executable (Universal Binary)..."

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

# Build the executable with universal2 target
echo "Building universal executable from app_refactored.spec..."
echo "This will create a binary that works on both Intel and Apple Silicon Macs..."
pyinstaller app_refactored.spec

# Check if build was successful
if [ -d "dist/UniteToolbox.app" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "✓ Executable created at: dist/UniteToolbox.app"
    echo ""
    echo "To run the app, double-click UniteToolbox.app or run:"
    echo "  open dist/UniteToolbox.app"
else
    echo ""
    echo "✗ Build failed. Check the output above for errors."
    exit 1
fi

