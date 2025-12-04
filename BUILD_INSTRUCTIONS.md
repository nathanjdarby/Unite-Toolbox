# Building the Unite Toolbox Executables

This guide explains how to build standalone executables for the Unite Toolbox applications.

## Prerequisites

1. **Python 3.7 or higher** - For universal binary support, use a **Universal2 Python** installation from [python.org](https://www.python.org/downloads/) (recommended)
2. All dependencies from `requirements.txt`
3. PyInstaller (will be installed automatically by the build script)

**Note for Universal Binaries**: The build creates a universal binary that works on both Intel and Apple Silicon Macs. For this to work properly, you should use a Universal2 Python installation. If you're using a single-architecture Python, the build will still work but may only support your current architecture.

## Building the GUI Application

### Quick Build

Run the build script:

```bash
./build_executable.sh
```

This creates `UniteToolbox.app` - the desktop GUI application.

### Manual Build

```bash
# Install PyInstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller app_refactored.spec
```

## Building the Flask Web Application

### Quick Build

Run the Flask build script:

```bash
./build_flask_executable.sh
```

This creates `UniteToolboxWeb.app` - a standalone web server that:
- Starts the Flask web server automatically
- Opens your browser to `http://127.0.0.1:5000`
- Works on both Intel and Apple Silicon Macs

### Manual Build

```bash
pyinstaller flask_app.spec
```

## Output

After building, the executables will be located at:

### GUI Application
- **macOS**: `dist/UniteToolbox.app` (double-click to run)
  - **Universal Binary**: Works on both Intel (x86_64) and Apple Silicon (arm64) Macs

### Web Application
- **macOS**: `dist/UniteToolboxWeb.app` (double-click to run)
  - **Universal Binary**: Works on both Intel (x86_64) and Apple Silicon (arm64) Macs
  - Automatically starts server and opens browser

- **Windows**: `dist/UniteToolbox.exe` / `dist/UniteToolboxWeb.exe`
- **Linux**: `dist/UniteToolbox` / `dist/UniteToolboxWeb`

## Manual Build Steps

If you prefer to build manually:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. Build using the spec file:

   ```bash
   pyinstaller app_refactored.spec
   ```

3. The executable will be in the `dist/` folder.

## Distribution

To distribute the application:

- **macOS**: Share the entire `UniteToolbox.app` bundle
- **Windows**: Share the `UniteToolbox.exe` file
- **Linux**: Share the `UniteToolbox` executable

Note: Users do not need Python installed to run the executable.

## Troubleshooting

If the build fails:

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check that PyInstaller is up to date: `pip install --upgrade pyinstaller`
3. Review the build output for specific error messages
4. Try building with console enabled (change `console=False` to `console=True` in the spec file) to see error messages

### Universal Binary Issues

If you encounter issues building a universal binary:

- **Use Universal2 Python**: Download and install Python from [python.org](https://www.python.org/downloads/) which provides Universal2 installers
- **Check dependencies**: Some packages may not have universal binary support. You may need to install universal versions
- **Build separately**: If universal build fails, you can build separate versions:
  - For Intel: `pyinstaller --target-arch x86_64 app_refactored.spec`
  - For Apple Silicon: `pyinstaller --target-arch arm64 app_refactored.spec`
