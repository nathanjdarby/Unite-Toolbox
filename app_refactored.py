"""
Refactored main application     for Unite Toolbox.
Clean, modular implementation with separated concerns.
"""

import tkinter as tk
import subprocess
import os
import pyperclip
from typing import Optional

from config import JOTFORM_TEMPLATES, APP_SETTINGS
from utils import DataProcessor, HTMLProcessor, FileHandler
from gui_components import DialogHelper, MenuBuilder, ButtonGrid


class UniteToolboxApp:
    """Main application class for Unite Toolbox."""
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.setup_window()
        self.setup_menu()
        self.setup_gui()
    
    def setup_window(self):
        """Configure the main window."""
        self.root.geometry(APP_SETTINGS["geometry"])
        self.root.title(APP_SETTINGS["title"])
        self.root.attributes("-topmost", APP_SETTINGS["topmost"])
    
    def setup_menu(self):
        """Create the application menu bar."""
        menu_bar = tk.Menu(self.root)
        jotform_menu = MenuBuilder.create_jotform_menu(
            menu_bar, 
            JOTFORM_TEMPLATES, 
            self.launch_validator
        )
        menu_bar.add_cascade(label="JotForm", menu=jotform_menu)
        self.root.config(menu=menu_bar)
    
    def setup_gui(self):
        """Create the main GUI components."""
        # Create button grid for organized layout
        button_grid = ButtonGrid(self.root, columns=3)
        
        # CSV Tools Section
        button_grid.add_label("CSV Tools")
        button_grid.new_row()
        
        button_grid.add_button("CSV 2 UWP", self.convert_csv_to_uwp)
        button_grid.add_button("CSV 2 SMS List", self.create_sms_list)
        button_grid.add_button("CSV Divide by Workplace", self.divide_by_workplace)
        
        # HTML Tools Section
        button_grid.new_row()
        button_grid.add_label("HTML Tools")
        button_grid.new_row()
        
        button_grid.add_button("Process HTML File", self.process_html_file)
    
    def launch_validator(self):
        """Launch the JotForm validator application."""
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            validator_path = os.path.join(script_dir, 'validate-jot.py')
            subprocess.Popen(['python3', validator_path])
        except Exception as e:
            DialogHelper.show_error(f"Failed to launch validator: {e}")
    
    def convert_csv_to_uwp(self):
        """Convert CSV file to UWP format."""
        try:
            # Select input file
            input_file = DialogHelper.select_file("Select CSV file to convert")
            if not input_file:
                return
            
            # Load and process data
            df = DataProcessor.load_data_file(input_file)
            df_uwp = DataProcessor.convert_csv_to_uwp(df)
            
            # Select output file
            output_file = DialogHelper.select_save_file(
                "Save UWP file as",
                default_extension=".csv"
            )
            if not output_file:
                return
            
            # Save processed data
            DataProcessor.save_data_file(df_uwp, output_file)
            # Clean up memory
            del df, df_uwp
            DialogHelper.show_info(f"File converted and saved to: {output_file}")
            
        except ValueError as e:
            DialogHelper.show_error(str(e))
        except Exception as e:
            DialogHelper.show_error(f"An error occurred: {e}")
    
    def create_sms_list(self):
        """Create SMS list from data file."""
        try:
            # Select input file
            input_file = DialogHelper.select_file("Select data file for SMS list")
            if not input_file:
                return
            
            # Load and process data
            df = DataProcessor.load_data_file(input_file)
            sms_df = DataProcessor.create_sms_list(df)
            
            # Select output file
            output_file = DialogHelper.select_save_file(
                "Save SMS list as",
                default_extension=".csv"
            )
            if not output_file:
                return
            
            # Save SMS list
            DataProcessor.save_data_file(sms_df, output_file)
            # Clean up memory
            del df, sms_df
            # Open the saved file
            os.system(f'open "{output_file}"')
            DialogHelper.show_info(f"SMS list saved and opened: {output_file}")
            
        except Exception as e:
            DialogHelper.show_error(f"An error occurred: {e}")
    
    def divide_by_workplace(self):
        """Divide data file by workplace."""
        try:
            # Select input file
            input_file = DialogHelper.select_file("Select data file to divide")
            if not input_file:
                return
            
            # Load data
            df = DataProcessor.load_data_file(input_file)
            
            # Check if workplace column exists
            workplace_column = "Workplace Name"
            if workplace_column not in df.columns:
                DialogHelper.show_error(f"Workplace column '{workplace_column}' not found in the file.")
                return
            
            # Select output directory
            output_dir = DialogHelper.select_directory("Select directory to save workplace files")
            if not output_dir:
                return
            
            # Divide by workplace
            workplaces = DataProcessor.divide_by_workplace(df, workplace_column)
            
            # Save individual files
            file_extension = '.xlsx' if input_file.endswith('.xlsx') else '.csv'
            num_workplaces = len(workplaces)
            for workplace_name, workplace_df in workplaces.items():
                safe_filename = FileHandler.get_safe_filename(workplace_name)
                output_file = os.path.join(output_dir, f"{safe_filename}{file_extension}")
                DataProcessor.save_data_file(workplace_df, output_file)
                # Clean up memory after each file
                del workplace_df
            
            # Clean up main dataframe
            del df, workplaces
            DialogHelper.show_info(f"Created {num_workplaces} workplace files in: {output_dir}")
            
        except Exception as e:
            DialogHelper.show_error(f"An error occurred: {e}")
    
    def process_html_file(self):
        """Process HTML file by removing MSO code and inlining CSS."""
        try:
            # Select input file
            input_file = DialogHelper.select_file(
                "Select HTML file to process",
                file_types=[("HTML files", "*.html")]
            )
            if not input_file:
                return
            
            # Read HTML content
            with open(input_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Process HTML
            processed_html = HTMLProcessor.process_html(html_content)
            
            # Select output file
            output_file = DialogHelper.select_save_file(
                "Save processed HTML as",
                default_extension=".html",
                file_types=[("HTML files", "*.html")]
            )
            if not output_file:
                return
            
            # Save processed HTML
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(processed_html)
            
            # Copy to clipboard
            pyperclip.copy(processed_html)
            
            DialogHelper.show_info("HTML processed successfully and copied to clipboard!")
            
        except Exception as e:
            DialogHelper.show_error(f"An error occurred: {e}")
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point for the application."""
    app = UniteToolboxApp()
    app.run()


if __name__ == "__main__":
    main() 