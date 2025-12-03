# Running the Flask Web Application

The Flask web application provides a web-based interface for the Unite Toolbox tools. The Flask app files are stored in the `archive/` folder but can be run easily.

## Quick Start

### Option 1: Using the Run Script (Recommended)

Simply run:
```bash
./run_flask_app.sh
```

This script will:
- Check for Flask installation
- Set up necessary directories
- Start the Flask server
- Open the app at `http://127.0.0.1:5000`

### Option 2: Manual Setup

1. **Copy Flask files to main directory** (temporary):
   ```bash
   cp archive/flask_app.py .
   cp -r archive/templates .
   ```

2. **Create required directories**:
   ```bash
   mkdir -p uploads results
   ```

3. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

4. **Run the Flask app**:
   ```bash
   python flask_app.py
   ```

5. **Access the web interface**:
   Open your browser and go to: `http://127.0.0.1:5000`

6. **Clean up** (after you're done):
   ```bash
   rm flask_app.py
   rm -r templates
   ```

## Features Available in Flask App

- **CSV to UWP**: Convert CSV files to UWP format
- **CSV to SMS List**: Create SMS lists from CSV data
- **CSV Divide by Workplace**: Split CSV files by workplace
- **HTML Processing**: Remove MSO code and inline CSS
- **URL Builder**: Generate survey URLs with parameters
- **CSV Compare**: Compare two CSV files to find missing records

## Requirements

- Python 3.7+
- Flask (install with `pip install flask`)
- All dependencies from `requirements.txt`

## Notes

- The Flask app uses the same `config.py` and `utils.py` modules as the main GUI application
- Uploaded files are stored in the `uploads/` folder
- Processed results are stored in the `results/` folder
- The app runs in debug mode by default (auto-reloads on code changes)

