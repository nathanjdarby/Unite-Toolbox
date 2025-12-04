# Unite Toolbox - Refactored Version

A clean, modular implementation of the Unite Toolbox application with improved code organization, maintainability, and extensibility.

## 🚀 Features

- **CSV Processing**: Convert CSV files to UWP format, create SMS lists, and divide by workplace
- **HTML Processing**: Remove MSO code and inline CSS for email compatibility
- **URL Building**: Generate survey URLs with customizable parameters
- **Data Comparison**: Compare CSV files to find missing records
- **JotForm Integration**: Access to JotForm templates and validator

## 📁 Project Structure

```
Unite Toolbox/
├── config.py                 # Configuration and constants
├── utils.py                  # Core business logic and utilities
├── gui_components.py         # Reusable GUI components
├── app_refactored.py         # Main application (refactored)
├── compare_refactored.py     # CSV comparison tool (refactored)
├── urlbuilder_refactored.py  # URL builder (refactored)
├── validate-jot.py          # JotForm validator (original)
├── templates.py             # HTML templates (original)
├── requirements.txt         # Python dependencies
└── README_REFACTORED.md     # This file
```

## 🏗️ Architecture

### Separation of Concerns

The refactored codebase follows clean architecture principles:

- **Configuration** (`config.py`): All constants, settings, and data mappings
- **Business Logic** (`utils.py`): Core data processing and utility functions
- **GUI Components** (`gui_components.py`): Reusable UI elements and dialogs
- **Applications**: Clean, focused application classes

### Key Improvements

1. **No Global Variables**: All state is properly encapsulated
2. **Type Hints**: Full type annotation for better IDE support
3. **Error Handling**: Consistent error handling patterns
4. **Documentation**: Comprehensive docstrings for all functions
5. **Modularity**: Each component has a single responsibility
6. **Reusability**: Common functionality is extracted into reusable classes

## 🛠️ Installation

1. **Clone or download** the project files
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Main Application

Run the refactored main application:

```bash
python app_refactored.py
```

### CSV Comparison Tool

Run the CSV comparison tool:

```bash
python compare_refactored.py
```

### URL Builder

Run the URL builder application:

```bash
python urlbuilder_refactored.py
```

### JotForm Validator

Run the JotForm validator:

```bash
python validate-jot.py
```

## 📋 Core Components

### DataProcessor Class

Handles all CSV and Excel file operations:

```python
from utils import DataProcessor

# Load a data file
df = DataProcessor.load_data_file("data.csv")

# Convert to UWP format
uwp_df = DataProcessor.convert_csv_to_uwp(df)

# Create SMS list
sms_df = DataProcessor.create_sms_list(df)

# Divide by workplace
workplaces = DataProcessor.divide_by_workplace(df)
```

### HTMLProcessor Class

Handles HTML processing operations:

```python
from utils import HTMLProcessor

# Process HTML content
processed_html = HTMLProcessor.process_html(html_content)
```

### URLBuilder Class

Handles URL building operations:

```python
from utils import URLBuilder

# Build survey URL with parameters
url = URLBuilder.build_survey_url("form-path", {"FirstName": True, "LastName": True})
```

### DialogHelper Class

Provides consistent dialog functionality:

```python
from gui_components import DialogHelper

# Show file selection dialog
file_path = DialogHelper.select_file("Select CSV file")

# Show information message
DialogHelper.show_info("Operation completed successfully")

# Show error message
DialogHelper.show_error("An error occurred")
```

## 🔧 Configuration

All configuration is centralized in `config.py`:

- **JOTFORM_TEMPLATES**: URLs for JotForm templates
- **CSV_COLUMN_MAPPING**: Column mappings for UWP conversion
- **URL_BUILDER_PARAMS**: Parameters for URL building
- **APP_SETTINGS**: Application window settings
- **SUPPORTED_FILE_TYPES**: File type definitions

## 🧪 Testing

The modular structure makes it easy to test individual components:

```python
from utils import DataProcessor
import pandas as pd

# Test data processing
test_df = pd.DataFrame({
    "First Name": ["John"],
    "Surname": ["Doe"],
    "Member Number": ["12345"]
})

# Test UWP conversion
uwp_df = DataProcessor.convert_csv_to_uwp(test_df)
assert "FirstName" in uwp_df.columns
```

## 🔄 Migration from Original Code

### Key Changes

1. **No Global Variables**: All state is now properly encapsulated in classes
2. **Consistent Naming**: All functions follow snake_case convention
3. **Error Handling**: Proper exception handling with user-friendly messages
4. **Type Safety**: Full type annotations for better code quality
5. **Documentation**: Comprehensive docstrings for all functions

### Benefits

- **Maintainability**: Easier to understand and modify
- **Extensibility**: New features can be added without affecting existing code
- **Testability**: Individual components can be tested in isolation
- **Reusability**: Common functionality is shared across applications
- **Reliability**: Better error handling and validation

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **File Not Found**: Check that file paths are correct and files exist
3. **Permission Errors**: Ensure you have write permissions for output directories

### Getting Help

- Check the error messages for specific details
- Verify that input files have the expected format
- Ensure all required columns are present in CSV files

## 📝 Contributing

When adding new features:

1. **Follow the modular structure** - add business logic to `utils.py`
2. **Use type hints** - annotate all function parameters and return values
3. **Add documentation** - include docstrings for all new functions
4. **Update configuration** - add new constants to `config.py`
5. **Test thoroughly** - ensure new functionality works as expected

## 📄 License

This project is for internal use by Unite the Union.

---

**Note**: This refactored version maintains full compatibility with the original functionality while providing a much cleaner and more maintainable codebase.
