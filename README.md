# Unite Toolbox

A Python application for processing CSV files, HTML content, and managing JotForm integrations.

## Essential Files

### Core Application
- `app_refactored.py` - Main application entry point
- `config.py` - Configuration and constants
- `utils.py` - Core business logic and utilities
- `gui_components.py` - Reusable GUI components
- `validate-jot.py` - JotForm validator script

### Build & Documentation
- `app_refactored.spec` - PyInstaller spec file for creating executables
- `build_executable.sh` - Build script for creating standalone executables
- `BUILD_INSTRUCTIONS.md` - Instructions for building the executable
- `requirements.txt` - Python dependencies

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GUI application:**
   ```bash
   python app_refactored.py
   ```

3. **Run the Flask web application:**
   ```bash
   ./run_flask_app.sh
   ```
   Then open `http://127.0.0.1:5000` in your browser.
   See `FLASK_APP_INSTRUCTIONS.md` for more details.

4. **Build executables:**
   ```bash
   # Build GUI application
   ./build_executable.sh
   
   # Build Flask web application
   ./build_flask_executable.sh
   ```
   
   The Flask executable will automatically start the server and open your browser!

## Features

- **CSV to UWP**: Convert CSV files to UWP format
- **CSV to SMS List**: Create SMS lists from CSV data
- **CSV Divide by Workplace**: Split CSV files by workplace
- **HTML Processing**: Remove MSO code and inline CSS
- **JotForm Integration**: Access JotForm templates and validator

## Archived Files

Non-essential files have been moved to the `archive/` folder, including:
- Flask web application files
- Separate tool scripts (compare, urlbuilder)
- Test files
- Build artifacts
- Old documentation

See `archive/README.md` for details.

