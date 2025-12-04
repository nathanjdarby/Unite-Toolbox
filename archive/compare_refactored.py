"""
Refactored CSV comparison tool.
Clean, modular implementation for comparing CSV files.
"""

from utils import DataProcessor
from gui_components import DialogHelper, FileHandler


def compare_csv_files():
    """
    Compare two CSV files and find records that exist in the first but not in the second.
    """
    try:
        # Select the first CSV file
        file1_path = DialogHelper.select_file("Select the first CSV file")
        if not file1_path:
            return
        
        # Select the second CSV file
        file2_path = DialogHelper.select_file("Select the second CSV file")
        if not file2_path:
            return
        
        # Load both CSV files
        df1 = DataProcessor.load_data_file(file1_path)
        df2 = DataProcessor.load_data_file(file2_path)
        
        # Get the membership column name from user
        membership_column = DialogHelper.show_input_dialog(
            "Please enter the name of the membership column:"
        )
        if not membership_column:
            return
        
        # Validate that the column exists in both files
        if membership_column not in df1.columns or membership_column not in df2.columns:
            DialogHelper.show_error(
                f"The specified membership column '{membership_column}' "
                f"is not present in one or both CSV files."
            )
            return
        
        # Compare the DataFrames
        missing_records = DataProcessor.compare_dataframes(df1, df2, membership_column)
        
        if missing_records.empty:
            DialogHelper.show_info("No missing rows found.")
            return
        
        # Create output directory if it doesn't exist
        output_dir = "CompareResults"
        FileHandler.ensure_directory_exists(output_dir)
        
        # Select save location
        save_path = DialogHelper.select_save_file(
            "Save missing records as",
            default_extension=".csv",
            file_types=[("CSV files", "*.csv")]
        )
        if not save_path:
            return
        
        # Save the missing records
        DataProcessor.save_data_file(missing_records, save_path)
        DialogHelper.show_info(f"Missing rows have been saved to '{save_path}'.")
        
    except Exception as e:
        DialogHelper.show_error(f"An error occurred: {e}")


def main():
    """Main entry point for the comparison tool."""
    compare_csv_files()


if __name__ == "__main__":
    main() 