# Archive Folder

This folder contains non-essential files that have been archived to keep the main project directory clean.

## Contents

### Flask Web Application
- `flask_app.py` - Flask web application (separate from main GUI app)
- `templates/` - HTML templates for Flask app
- `unite_toolbox.spec` - PyInstaller spec file for Flask app

### Separate Tools
- `compare_refactored.py` - CSV comparison tool (standalone)
- `urlbuilder_refactored.py` - URL builder tool (standalone)
- `test_refactored.py` - Test scripts

### Build Artifacts
- `build/` - PyInstaller build artifacts
- `dist/` - Previous build output
- `dist 2/` - Another previous build output

### Cache and Temporary Files
- `__pycache__/` - Python bytecode cache
- `results/` - Temporary results directory
- `uploads/` - Temporary uploads directory

### Documentation
- `README_REFACTORED.md` - Old documentation (replaced by BUILD_INSTRUCTIONS.md)

### Other
- `UniteToolbox_Standalone.zip` - Old standalone zip file
- `venv/` - Python virtual environment (should be recreated as needed)

## Note

These files are kept for reference but are not required for the main application to run. The main application (`app_refactored.py`) only requires:
- `config.py`
- `utils.py`
- `gui_components.py`
- `validate-jot.py`
- `requirements.txt`

