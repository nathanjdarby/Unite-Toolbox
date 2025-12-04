"""
Test script for the refactored Unite Toolbox components.
Demonstrates the new modular structure and functionality.
"""

import pandas as pd
from utils import DataProcessor, HTMLProcessor, URLBuilder, FileHandler
from config import CSV_COLUMN_MAPPING, URL_BUILDER_PARAMS, JOTFORM_TEMPLATES


def test_data_processor():
    """Test the DataProcessor class functionality."""
    print("Testing DataProcessor...")
    
    # Create test data
    test_data = {
        "First Name": ["John", "Jane", "Bob"],
        "Surname": ["Doe", "Smith", "Johnson"],
        "Member Number": ["12345", "67890", "11111"],
        "Address - Home - Line 1": ["123 Main St", "456 Oak Ave", "789 Pine Rd"],
        "Address - Home - Line 2": ["Apt 1", "Unit 2", "Suite 3"],
        "Address - Home - Line 3": ["", "", ""],
        "Address - Home - Line 4": ["", "", ""],
        "Address - Home PC": ["AB12 3CD", "EF45 6GH", "IJ78 9KL"],
        "Employer Name": ["Company A", "Company B", "Company C"],
        "Employer": ["EMP001", "EMP002", "EMP003"],
        "Workplace Name": ["Workplace 1", "Workplace 2", "Workplace 1"],
        "Workplace": ["WP001", "WP002", "WP001"],
        "Region": ["North", "South", "North"],
        "Job Description ": ["Manager", "Worker", "Supervisor"],
        "Email Address": ["john@example.com", "jane@example.com", "bob@example.com"],
        "Allow Email": ["Y", "Y", "N"],
        "Allow Phone": ["Y", "N", "Y"],
        "Allow SMS": ["Y", "Y", "Y"],
        "Home phone": ["01234567890", "09876543210", "05551234567"],
        "Mobile phone": ["07123456789", "07987654321", "07778889999"],
        "TPS Flag": ["N", "N", "N"]
    }
    
    df = pd.DataFrame(test_data)
    
    # Test UWP conversion
    try:
        uwp_df = DataProcessor.convert_csv_to_uwp(df)
        print(f"✓ UWP conversion successful. Output columns: {list(uwp_df.columns)}")
    except Exception as e:
        print(f"✗ UWP conversion failed: {e}")
    
    # Test workplace division
    try:
        workplaces = DataProcessor.divide_by_workplace(df)
        print(f"✓ Workplace division successful. Found {len(workplaces)} workplaces")
        for workplace, workplace_df in workplaces.items():
            print(f"  - {workplace}: {len(workplace_df)} records")
    except Exception as e:
        print(f"✗ Workplace division failed: {e}")
    
    # Test SMS list creation
    try:
        sms_df = DataProcessor.create_sms_list(df)
        print(f"✓ SMS list creation successful. Found {len(sms_df)} SMS-eligible records")
    except Exception as e:
        print(f"✗ SMS list creation failed: {e}")


def test_html_processor():
    """Test the HTMLProcessor class functionality."""
    print("\nTesting HTMLProcessor...")
    
    # Test HTML with MSO code
    test_html = """
    <html>
    <head>
        <style>
            body { color: red; }
        </style>
    </head>
    <body>
        <!--[if mso]>
        <p>MSO specific content</p>
        <![endif]-->
        <p style="font-size: 12px;">Hello World</p>
    </body>
    </html>
    """
    
    try:
        processed_html = HTMLProcessor.process_html(test_html)
        print("✓ HTML processing successful")
        print(f"  - Original length: {len(test_html)} characters")
        print(f"  - Processed length: {len(processed_html)} characters")
        print(f"  - MSO code removed: {'<!--[if mso]' not in processed_html}")
    except Exception as e:
        print(f"✗ HTML processing failed: {e}")


def test_url_builder():
    """Test the URLBuilder class functionality."""
    print("\nTesting URLBuilder...")
    
    # Test URL building with parameters
    base_path = "form-templates/standalone/ur/test-form"
    parameters = {
        "FirstName": True,
        "LastName": True,
        "MembershipNumber": False,
        "EmailAddress": True
    }
    
    try:
        url = URLBuilder.build_survey_url(base_path, parameters)
        print("✓ URL building successful")
        print(f"  - Base path: {base_path}")
        print(f"  - Parameters: {parameters}")
        print(f"  - Generated URL: {url}")
    except Exception as e:
        print(f"✗ URL building failed: {e}")


def test_file_handler():
    """Test the FileHandler class functionality."""
    print("\nTesting FileHandler...")
    
    # Test safe filename generation
    test_filenames = [
        "Normal File Name",
        "File with <invalid> characters",
        "File with : invalid : chars",
        "File with spaces and dots...",
        "File/with\\path?chars*"
    ]
    
    for filename in test_filenames:
        safe_name = FileHandler.get_safe_filename(filename)
        print(f"  '{filename}' -> '{safe_name}'")


def test_configuration():
    """Test the configuration constants."""
    print("\nTesting Configuration...")
    
    print(f"✓ JOTFORM_TEMPLATES: {len(JOTFORM_TEMPLATES)} templates defined")
    print(f"✓ CSV_COLUMN_MAPPING: {len(CSV_COLUMN_MAPPING['columns_to_keep'])} columns to keep")
    print(f"✓ URL_BUILDER_PARAMS: {len(URL_BUILDER_PARAMS)} parameters available")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing Refactored Unite Toolbox Components")
    print("=" * 50)
    
    test_configuration()
    test_data_processor()
    test_html_processor()
    test_url_builder()
    test_file_handler()
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)


if __name__ == "__main__":
    main() 