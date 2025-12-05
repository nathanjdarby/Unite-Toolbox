from flask import Flask, render_template, request, redirect, url_for, send_file, flash, session
import os
import sys
import io
import json
from werkzeug.utils import secure_filename

# Lazy load heavy dependencies
_pandas = None
_config_cache = None

def _get_pandas():
    """Lazy load pandas for faster startup."""
    global _pandas
    if _pandas is None:
        import pandas as pd
        _pandas = pd
    return _pandas

def _get_config():
    """Cache config imports."""
    global _config_cache
    if _config_cache is None:
        from config import JOTFORM_TEMPLATES, URL_BUILDER_PARAMS, CSV_COLUMN_MAPPING
        _config_cache = {
            'JOTFORM_TEMPLATES': JOTFORM_TEMPLATES,
            'URL_BUILDER_PARAMS': URL_BUILDER_PARAMS,
            'CSV_COLUMN_MAPPING': CSV_COLUMN_MAPPING
        }
    return _config_cache

# Import utils (now optimized with lazy loading)
from utils import DataProcessor, HTMLProcessor, URLBuilder, FileHandler

app = Flask(__name__)
app.secret_key = 'unite-toolbox-secret-key'  # For flash messages

# Handle paths for both development and PyInstaller executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = sys._MEIPASS
    APP_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    APP_DIR = BASE_DIR

UPLOAD_FOLDER = os.path.join(APP_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(APP_DIR, 'results')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

@app.route('/')
def home():
    config = _get_config()
    return render_template('home.html', jotform_templates=config['JOTFORM_TEMPLATES'])

@app.route('/csv2uwp', methods=['GET', 'POST'])
def csv2uwp():
    if request.method == 'POST':
        # Check if this is the column mapping step
        if 'column_mapping' in request.form:
            # Process with custom column mapping
            try:
                column_mapping_json = request.form.get('column_mapping')
                column_mapping = json.loads(column_mapping_json)
                
                # Get the stored file path from session
                if 'data_file_path' not in session:
                    flash('Session expired. Please upload the file again.', 'danger')
                    return redirect(url_for('csv2uwp'))
                
                # Read the file again (supports both CSV and Excel)
                file_path = session['data_file_path']
                df = DataProcessor.load_data_file(file_path)
                
                # Convert with custom mapping
                df_uwp = DataProcessor.convert_csv_to_uwp(df, column_mapping=column_mapping)
                
                # Clean up temporary file
                if os.path.exists(file_path):
                    os.remove(file_path)
                session.pop('data_file_path', None)
                session.pop('data_columns', None)
                
                # Return converted file (optimized CSV writing)
                output = io.StringIO()
                df_uwp.to_csv(output, index=False, lineterminator='\n')
                output.seek(0)
                return send_file(
                    io.BytesIO(output.getvalue().encode()),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name='uwp_converted.csv'
                )
            except Exception as e:
                flash(f'Error converting file: {e}', 'danger')
                return redirect(url_for('csv2uwp'))
        else:
            # Initial file upload step
            file = request.files.get('data_file')
            if not file or file.filename == '':
                flash('No file selected', 'danger')
                return redirect(request.url)
            try:
                # Save file temporarily
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, f'temp_{filename}')
                file.save(file_path)
                
                # Read file to get columns (supports both CSV and Excel)
                df = DataProcessor.load_data_file(file_path)
                
                # Store file path and columns in session
                session['data_file_path'] = file_path
                session['data_columns'] = list(df.columns)
                
                # Get UWP output columns
                uwp_columns = DataProcessor.get_uwp_output_columns()
                
                # Try to auto-map columns based on default mapping (cached)
                config = _get_config()
                default_mapping = config['CSV_COLUMN_MAPPING']["new_column_names"]
                reverse_mapping = {v: k for k, v in default_mapping.items()}
                auto_mapping = {}
                for uwp_col in uwp_columns:
                    # Try to find matching CSV column
                    default_source = reverse_mapping.get(uwp_col, '')
                    if default_source in df.columns:
                        auto_mapping[uwp_col] = default_source
                    else:
                        # Try fuzzy matching
                        for csv_col in df.columns:
                            if csv_col.lower() == default_source.lower() or \
                               default_source.lower() in csv_col.lower() or \
                               csv_col.lower() in default_source.lower():
                                auto_mapping[uwp_col] = csv_col
                                break
                
                return render_template('csv2uwp_map.html', 
                                     csv_columns=session['data_columns'],
                                     uwp_columns=uwp_columns,
                                     auto_mapping=auto_mapping)
            except Exception as e:
                flash(f'Error reading file: {e}', 'danger')
    return render_template('csv2uwp.html')

@app.route('/csv2sms', methods=['GET', 'POST'])
def csv2sms():
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        try:
            pd = _get_pandas()
            df = pd.read_csv(file, engine='c', low_memory=False)
            sms_df = DataProcessor.create_sms_list(df)
            output = io.StringIO()
            sms_df.to_csv(output, index=False, lineterminator='\n')
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='sms_list.csv'
            )
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('csv2sms.html')

@app.route('/csvdivide', methods=['GET', 'POST'])
def csvdivide():
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        try:
            pd = _get_pandas()
            df = pd.read_csv(file, engine='c', low_memory=False)
            workplaces = DataProcessor.divide_by_workplace(df)
            # Create a zip of all workplace files
            import zipfile
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zipf:
                for name, wdf in workplaces.items():
                    safe_name = FileHandler.get_safe_filename(name) or 'workplace'
                    csv_bytes = wdf.to_csv(index=False).encode()
                    zipf.writestr(f'{safe_name}.csv', csv_bytes)
            zip_buffer.seek(0)
            return send_file(
                zip_buffer,
                mimetype='application/zip',
                as_attachment=True,
                download_name='workplaces.zip'
            )
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('csvdivide.html')

@app.route('/htmlprocess', methods=['GET', 'POST'])
def htmlprocess():
    if request.method == 'POST':
        file = request.files.get('html_file')
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        try:
            html_content = file.read().decode('utf-8')
            processed_html = HTMLProcessor.process_html(html_content)
            return send_file(
                io.BytesIO(processed_html.encode()),
                mimetype='text/html',
                as_attachment=True,
                download_name='processed.html'
            )
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('htmlprocess.html')

@app.route('/urlbuilder', methods=['GET', 'POST'])
def urlbuilder():
    url = None
    config = _get_config()
    url_builder_params = config['URL_BUILDER_PARAMS']
    if request.method == 'POST':
        base_path = request.form.get('base_path', '').strip()
        params = {k: (k in request.form) for k in url_builder_params.keys()}
        try:
            url = URLBuilder.build_survey_url(base_path, params)
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('urlbuilder.html', url=url, params=url_builder_params)

@app.route('/csvcompare', methods=['GET', 'POST'])
def csvcompare():
    if request.method == 'POST':
        file1 = request.files.get('csv_file1')
        file2 = request.files.get('csv_file2')
        key_column = request.form.get('key_column', '').strip()
        if not file1 or not file2 or not key_column:
            flash('Please provide both files and the key column.', 'danger')
            return redirect(request.url)
        try:
            pd = _get_pandas()
            df1 = pd.read_csv(file1, engine='c', low_memory=False)
            df2 = pd.read_csv(file2, engine='c', low_memory=False)
            missing = DataProcessor.compare_dataframes(df1, df2, key_column)
            output = io.StringIO()
            missing.to_csv(output, index=False, lineterminator='\n')
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='missing_rows.csv'
            )
        except Exception as e:
            flash(f'Error: {e}', 'danger')
    return render_template('csvcompare.html')

def open_browser():
    """Open the default browser to the Flask app URL."""
    import webbrowser
    import time
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    import threading
    print("Starting Unite Toolbox Flask App...")
    print("App will be available at: http://127.0.0.1:5000")
    print("Opening browser automatically...")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run Flask app (use_threaded=False for PyInstaller compatibility)
    app.run(debug=False, port=5000, use_reloader=False) 