"""
Refactored URL Builder for Unite Toolbox.
Clean, modular implementation for building survey URLs with parameters.
"""

import tkinter as tk
from tkinter import ttk
import pyperclip
import webbrowser
from typing import Dict, List

from config import URL_BUILDER_PARAMS, BASE_SURVEY_URL
from utils import URLBuilder
from gui_components import DialogHelper


class URLBuilderApp:
    """URL Builder application with GUI."""
    
    def __init__(self):
        """Initialize the URL Builder application."""
        self.root = tk.Tk()
        self.setup_window()
        self.setup_gui()
        self.url = ""
    
    def setup_window(self):
        """Configure the main window."""
        self.root.title("URL Builder")
        self.root.geometry("600x800")
        self.root.resizable(True, True)
    
    def setup_gui(self):
        """Create the GUI components."""
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas and scrollbar for scrollable content
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # URL input section
        self.create_url_input_section(scrollable_frame)
        
        # Parameters section
        self.create_parameters_section(scrollable_frame)
        
        # Buttons section
        self.create_buttons_section(scrollable_frame)
        
        # URL display section
        self.create_url_display_section(scrollable_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_url_input_section(self, parent):
        """Create the URL input section."""
        # URL input frame
        url_frame = ttk.LabelFrame(parent, text="Survey Path", padding="10")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        # URL input field
        ttk.Label(url_frame, text="Enter the survey path:").pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.pack(fill=tk.X, pady=(5, 0))
        self.url_entry.focus()
        
        # Example text
        example_text = "Example: form-templates/standalone/ur/anonymous-feedback-form-template"
        ttk.Label(url_frame, text=example_text, foreground="gray").pack(anchor=tk.W, pady=(5, 0))
    
    def create_parameters_section(self, parent):
        """Create the parameters selection section."""
        # Parameters frame
        params_frame = ttk.LabelFrame(parent, text="URL Parameters", padding="10")
        params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create checkboxes for each parameter
        self.param_vars = {}
        param_names = list(URL_BUILDER_PARAMS.keys())
        
        # Create a grid of checkboxes
        for i, param_name in enumerate(param_names):
            row = i // 2
            col = i % 2
            
            var = tk.BooleanVar()
            self.param_vars[param_name] = var
            
            checkbox = ttk.Checkbutton(
                params_frame, 
                text=param_name, 
                variable=var
            )
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
    
    def create_buttons_section(self, parent):
        """Create the buttons section."""
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Build URL button
        self.build_button = ttk.Button(
            buttons_frame, 
            text="Build URL", 
            command=self.build_url
        )
        self.build_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Copy to clipboard button
        self.copy_button = ttk.Button(
            buttons_frame, 
            text="Copy to Clipboard", 
            command=self.copy_to_clipboard,
            state="disabled"
        )
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Open in browser button
        self.open_button = ttk.Button(
            buttons_frame, 
            text="Open in Browser", 
            command=self.open_in_browser,
            state="disabled"
        )
        self.open_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        self.reset_button = ttk.Button(
            buttons_frame, 
            text="Reset", 
            command=self.reset_form
        )
        self.reset_button.pack(side=tk.LEFT)
    
    def create_url_display_section(self, parent):
        """Create the URL display section."""
        # URL display frame
        display_frame = ttk.LabelFrame(parent, text="Generated URL", padding="10")
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL text widget
        self.url_text = tk.Text(display_frame, height=8, wrap=tk.WORD)
        self.url_text.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar to text widget
        text_scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.url_text.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.url_text.configure(yscrollcommand=text_scrollbar.set)
    
    def build_url(self):
        """Build the URL with selected parameters."""
        try:
            # Get the base path from entry
            base_path = self.url_entry.get().strip()
            if not base_path:
                DialogHelper.show_error("Please enter a survey path.")
                return
            
            # Get selected parameters
            selected_params = {
                param_name: var.get()
                for param_name, var in self.param_vars.items()
            }
            
            # Build the URL
            self.url = URLBuilder.build_survey_url(base_path, selected_params)
            
            # Display the URL
            self.url_text.delete(1.0, tk.END)
            self.url_text.insert(1.0, self.url)
            
            # Enable buttons
            self.copy_button.config(state="normal")
            self.open_button.config(state="normal")
            
        except Exception as e:
            DialogHelper.show_error(f"Error building URL: {e}")
    
    def copy_to_clipboard(self):
        """Copy the generated URL to clipboard."""
        if self.url:
            try:
                pyperclip.copy(self.url)
                DialogHelper.show_info("URL copied to clipboard!")
            except Exception as e:
                DialogHelper.show_error(f"Error copying to clipboard: {e}")
        else:
            DialogHelper.show_warning("No URL generated yet. Please build the URL first.")
    
    def open_in_browser(self):
        """Open the generated URL in the default browser."""
        if self.url:
            try:
                webbrowser.open(self.url)
            except Exception as e:
                DialogHelper.show_error(f"Error opening browser: {e}")
        else:
            DialogHelper.show_warning("No URL generated yet. Please build the URL first.")
    
    def reset_form(self):
        """Reset the form to its initial state."""
        # Clear URL entry
        self.url_entry.delete(0, tk.END)
        
        # Uncheck all checkboxes
        for var in self.param_vars.values():
            var.set(False)
        
        # Clear URL display
        self.url_text.delete(1.0, tk.END)
        
        # Disable buttons
        self.copy_button.config(state="disabled")
        self.open_button.config(state="disabled")
        
        # Clear URL variable
        self.url = ""
        
        # Set focus back to URL entry
        self.url_entry.focus()
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point for the URL Builder."""
    app = URLBuilderApp()
    app.run()


if __name__ == "__main__":
    main() 