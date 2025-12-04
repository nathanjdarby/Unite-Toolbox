"""
GUI components for the Unite Toolbox application.
Contains reusable GUI elements and dialog functions.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from typing import Optional, List, Tuple, Callable
from config import SUPPORTED_FILE_TYPES


class DialogHelper:
    """Helper class for creating common dialogs."""
    
    @staticmethod
    def create_hidden_root() -> tk.Tk:
        """Create a hidden root window for dialogs."""
        root = tk.Tk()
        root.withdraw()
        return root
    
    @staticmethod
    def select_file(title: str = "Select File", 
                   file_types: List[Tuple[str, str]] = None) -> Optional[str]:
        """
        Show a file selection dialog.
        
        Args:
            title: Dialog title
            file_types: List of (description, pattern) tuples for file types
            
        Returns:
            Selected file path or None if cancelled
        """
        root = DialogHelper.create_hidden_root()
        if file_types is None:
            file_types = SUPPORTED_FILE_TYPES["all_data"]
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=file_types
        )
        root.destroy()
        return file_path if file_path else None
    
    @staticmethod
    def select_save_file(title: str = "Save File",
                        default_extension: str = ".csv",
                        file_types: List[Tuple[str, str]] = None) -> Optional[str]:
        """
        Show a file save dialog.
        
        Args:
            title: Dialog title
            default_extension: Default file extension
            file_types: List of (description, pattern) tuples for file types
            
        Returns:
            Selected save path or None if cancelled
        """
        root = DialogHelper.create_hidden_root()
        if file_types is None:
            file_types = SUPPORTED_FILE_TYPES["csv"]
        
        file_path = filedialog.asksaveasfilename(
            title=title,
            defaultextension=default_extension,
            filetypes=file_types
        )
        root.destroy()
        return file_path if file_path else None
    
    @staticmethod
    def select_directory(title: str = "Select Directory") -> Optional[str]:
        """
        Show a directory selection dialog.
        
        Args:
            title: Dialog title
            
        Returns:
            Selected directory path or None if cancelled
        """
        root = DialogHelper.create_hidden_root()
        directory_path = filedialog.askdirectory(title=title)
        root.destroy()
        return directory_path if directory_path else None
    
    @staticmethod
    def show_input_dialog(prompt: str, title: str = "Input") -> Optional[str]:
        """
        Show an input dialog.
        
        Args:
            prompt: Input prompt text
            title: Dialog title
            
        Returns:
            User input or None if cancelled
        """
        root = DialogHelper.create_hidden_root()
        user_input = simpledialog.askstring(title, prompt)
        root.destroy()
        return user_input
    
    @staticmethod
    def show_info(message: str, title: str = "Information") -> None:
        """Show an information message box."""
        root = DialogHelper.create_hidden_root()
        messagebox.showinfo(title, message, parent=root)
        root.destroy()
    
    @staticmethod
    def show_error(message: str, title: str = "Error") -> None:
        """Show an error message box."""
        root = DialogHelper.create_hidden_root()
        messagebox.showerror(title, message, parent=root)
        root.destroy()
    
    @staticmethod
    def show_warning(message: str, title: str = "Warning") -> None:
        """Show a warning message box."""
        root = DialogHelper.create_hidden_root()
        messagebox.showwarning(title, message, parent=root)
        root.destroy()


class MenuBuilder:
    """Helper class for building application menus."""
    
    @staticmethod
    def create_jotform_menu(parent: tk.Menu, 
                           templates: dict,
                           launch_validator_callback: Callable) -> tk.Menu:
        """
        Create the JotForm menu with templates and validator.
        
        Args:
            parent: Parent menu bar
            templates: Dictionary of template names and URLs
            launch_validator_callback: Callback function for launching validator
            
        Returns:
            Created JotForm menu
        """
        jotform_menu = tk.Menu(parent, tearoff=0)
        
        # Add validator option
        jotform_menu.add_command(label="Validator", command=launch_validator_callback)
        jotform_menu.add_separator()
        
        # Add templates submenu
        templates_menu = tk.Menu(jotform_menu, tearoff=0)
        for template_name, template_url in templates.items():
            templates_menu.add_command(
                label=template_name,
                command=lambda url=template_url: MenuBuilder._open_url(url)
            )
        
        jotform_menu.add_cascade(label="JotForm Templates", menu=templates_menu)
        return jotform_menu
    
    @staticmethod
    def _open_url(url: str) -> None:
        """Open a URL in the default browser."""
        import webbrowser
        webbrowser.open(url)


class ButtonGrid:
    """Helper class for creating organized button grids."""
    
    def __init__(self, parent: tk.Widget, columns: int = 3):
        """
        Initialize the button grid.
        
        Args:
            parent: Parent widget
            columns: Number of columns in the grid
        """
        self.parent = parent
        self.columns = columns
        self.current_row = 0
        self.current_col = 0
    
    def add_button(self, text: str, command: Callable, 
                   sticky: str = "w", padx: int = 5, pady: int = 5) -> tk.Button:
        """
        Add a button to the grid.
        
        Args:
            text: Button text
            command: Button command function
            sticky: Grid sticky option
            padx: Horizontal padding
            pady: Vertical padding
            
        Returns:
            Created button widget
        """
        button = tk.Button(self.parent, text=text, command=command)
        button.grid(
            column=self.current_col, 
            row=self.current_row, 
            sticky=sticky, 
            padx=padx, 
            pady=pady
        )
        
        # Move to next position
        self.current_col += 1
        if self.current_col >= self.columns:
            self.current_col = 0
            self.current_row += 1
        
        return button
    
    def add_label(self, text: str, sticky: str = "w", 
                  padx: int = 5, pady: int = 5) -> tk.Label:
        """
        Add a label to the grid.
        
        Args:
            text: Label text
            sticky: Grid sticky option
            padx: Horizontal padding
            pady: Vertical padding
            
        Returns:
            Created label widget
        """
        label = tk.Label(self.parent, text=text)
        label.grid(
            column=self.current_col, 
            row=self.current_row, 
            sticky=sticky, 
            padx=padx, 
            pady=pady
        )
        
        # Move to next position
        self.current_col += 1
        if self.current_col >= self.columns:
            self.current_col = 0
            self.current_row += 1
        
        return label
    
    def new_row(self) -> None:
        """Move to the next row."""
        self.current_col = 0
        self.current_row += 1 