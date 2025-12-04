"""
Utility functions for the Unite Toolbox application.
Contains common data processing and file handling functions.
Optimized for performance with lazy loading and caching.
"""

import os
import re
from typing import Optional, Dict, List, Tuple

# Lazy loading - import heavy dependencies only when needed
_pandas = None
_premailer_transform = None
_config_cache = None


def _get_pandas():
    """Lazy load pandas module."""
    global _pandas
    if _pandas is None:
        import pandas as pd
        _pandas = pd
    return _pandas


def _get_premailer():
    """Lazy load premailer transform function."""
    global _premailer_transform
    if _premailer_transform is None:
        from premailer import transform
        _premailer_transform = transform
    return _premailer_transform


def _get_config():
    """Cache config imports."""
    global _config_cache
    if _config_cache is None:
        from config import CSV_COLUMN_MAPPING, URL_BUILDER_PARAMS, BASE_SURVEY_URL
        _config_cache = {
            'CSV_COLUMN_MAPPING': CSV_COLUMN_MAPPING,
            'URL_BUILDER_PARAMS': URL_BUILDER_PARAMS,
            'BASE_SURVEY_URL': BASE_SURVEY_URL
        }
    return _config_cache


class DataProcessor:
    """Handles data processing operations for CSV and Excel files."""
    
    @staticmethod
    def load_data_file(file_path: str) -> 'pd.DataFrame':
        """
        Load a data file (CSV or Excel) into a pandas DataFrame.
        Optimized for performance with faster CSV engine.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            pandas DataFrame containing the file data
            
        Raises:
            ValueError: If file type is not supported
        """
        pd = _get_pandas()
        if file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            # Use faster C engine for CSV reading
            return pd.read_csv(file_path, engine='c', low_memory=False)
        else:
            raise ValueError("File type not supported. Please use .csv or .xlsx files.")
    
    @staticmethod
    def save_data_file(df: 'pd.DataFrame', file_path: str, file_type: str = None) -> None:
        """
        Save a DataFrame to a file.
        Optimized for performance.
        
        Args:
            df: DataFrame to save
            file_path: Path where to save the file
            file_type: Type of file to save ('csv' or 'xlsx'). If None, inferred from file_path
        """
        if file_type is None:
            file_type = 'xlsx' if file_path.endswith('.xlsx') else 'csv'
        
        if file_type == 'xlsx':
            df.to_excel(file_path, index=False, engine='openpyxl')
        else:
            # Use faster CSV writing
            df.to_csv(file_path, index=False, lineterminator='\n')
    
    @staticmethod
    def convert_csv_to_uwp(df: 'pd.DataFrame', column_mapping: Dict[str, str] = None) -> 'pd.DataFrame':
        """
        Convert CSV data to UWP format by keeping specific columns and renaming them.
        
        Args:
            df: Input DataFrame
            column_mapping: Optional custom mapping from CSV column names to UWP column names.
                          If None, uses default mapping from config.
            
        Returns:
            DataFrame with UWP format
        """
        config = _get_config()
        if column_mapping is None:
            # Use default mapping
            columns_to_keep = config['CSV_COLUMN_MAPPING']["columns_to_keep"]
            new_column_names = config['CSV_COLUMN_MAPPING']["new_column_names"]
            
            # Check if all required columns exist
            missing_columns = set(columns_to_keep) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Keep only required columns and rename them (avoid unnecessary copy if possible)
            df_uwp = df[columns_to_keep].copy()
            df_uwp.rename(columns=new_column_names, inplace=True)
        else:
            # Use custom mapping
            # Filter out None values (unmapped columns)
            valid_mapping = {k: v for k, v in column_mapping.items() if v is not None and v != ''}
            
            # Check if mapped columns exist in source DataFrame
            missing_columns = set(valid_mapping.keys()) - set(df.columns)
            if missing_columns:
                raise ValueError(f"Missing mapped columns: {', '.join(missing_columns)}")
            
            # Select and rename columns (avoid unnecessary copy if possible)
            df_uwp = df[list(valid_mapping.keys())].copy()
            df_uwp.rename(columns=valid_mapping, inplace=True)
        
        return df_uwp
    
    @staticmethod
    def get_uwp_output_columns() -> List[str]:
        """
        Get the list of required UWP output column names.
        Cached for performance.
        
        Returns:
            List of UWP output column names
        """
        config = _get_config()
        return list(config['CSV_COLUMN_MAPPING']["new_column_names"].values())
    
    @staticmethod
    def divide_by_workplace(df: 'pd.DataFrame', workplace_column: str = "Workplace Name") -> Dict[str, 'pd.DataFrame']:
        """
        Divide DataFrame by workplace, creating separate DataFrames for each workplace.
        
        Args:
            df: Input DataFrame
            workplace_column: Name of the column containing workplace information
            
        Returns:
            Dictionary mapping workplace names to their respective DataFrames
        """
        if workplace_column not in df.columns:
            raise ValueError(f"Workplace column '{workplace_column}' not found in DataFrame")
        
        workplaces = {}
        unique_workplaces = df[workplace_column].unique()
        
        pd = _get_pandas()
        for workplace in unique_workplaces:
            if pd.notna(workplace):  # Skip NaN values
                workplaces[workplace] = df[df[workplace_column] == workplace].copy()
        
        return workplaces
    
    @staticmethod
    def create_sms_list(df: 'pd.DataFrame') -> 'pd.DataFrame':
        """
        Create an SMS list from the input DataFrame.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame containing only SMS-eligible records
        """
        # Convert column names to lowercase for consistency
        df_lower = df.copy()
        df_lower.columns = df_lower.columns.str.lower()
        
        # Move home phone numbers starting with "07" or "7" to mobile phone
        home_phone_mask = (
            df_lower["home phone"].notna() & 
            df_lower["home phone"].astype(str).str.startswith(("07", "7"))
        )
        df_lower.loc[home_phone_mask, "mobile phone"] = df_lower.loc[home_phone_mask, "home phone"]
        
        # Filter for SMS-eligible records
        sms_eligible = df_lower[
            (df_lower["allow sms"] == "Y") & 
            df_lower["mobile phone"].notna()
        ]
        
        # Keep only relevant columns
        sms_columns = ["member number", "first name", "surname", "allow sms", "mobile phone"]
        return sms_eligible[sms_columns].copy()
    
    @staticmethod
    def compare_dataframes(df1: 'pd.DataFrame', df2: 'pd.DataFrame', 
                          key_column: str) -> 'pd.DataFrame':
        """
        Compare two DataFrames and find records that exist in df1 but not in df2.
        
        Args:
            df1: First DataFrame
            df2: Second DataFrame  
            key_column: Column to use for comparison
            
        Returns:
            DataFrame containing records from df1 that don't exist in df2
        """
        if key_column not in df1.columns or key_column not in df2.columns:
            raise ValueError(f"Key column '{key_column}' not found in one or both DataFrames")
        
        # Merge DataFrames to find differences
        merged = pd.merge(df1, df2, on=key_column, how='outer', indicator=True)
        
        # Find records that exist only in df1
        missing_records = merged[merged['_merge'] == 'left_only'].copy()
        
        # Remove the merge indicator column
        missing_records = missing_records.drop(columns=['_merge'])
        
        return missing_records


class HTMLProcessor:
    """Handles HTML processing operations."""
    
    @staticmethod
    def remove_mso_code(html_content: str) -> str:
        """
        Remove Microsoft Office (MSO) conditional comments from HTML.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            HTML content with MSO code removed
        """
        mso_regex = r'<!--\[if.*?\[endif\]-->'
        return re.sub(mso_regex, '', html_content, flags=re.DOTALL)
    
    @staticmethod
    def inline_css(html_content: str) -> str:
        """
        Inline CSS styles in HTML content.
        Uses lazy-loaded premailer for faster startup.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            HTML content with inlined CSS
        """
        transform = _get_premailer()
        return transform(html_content)
    
    @staticmethod
    def process_html(html_content: str) -> str:
        """
        Process HTML content by removing MSO code and inlining CSS.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            Processed HTML content
        """
        html_without_mso = HTMLProcessor.remove_mso_code(html_content)
        html_inlined = HTMLProcessor.inline_css(html_without_mso)
        return html_inlined


class URLBuilder:
    """Handles URL building operations."""
    
    @staticmethod
    def build_survey_url(base_path: str, parameters: Dict[str, bool]) -> str:
        """
        Build a survey URL with optional parameters.
        Uses cached config for performance.
        
        Args:
            base_path: Base path for the survey
            parameters: Dictionary mapping parameter names to boolean values
            
        Returns:
            Complete survey URL with parameters
        """
        config = _get_config()
        url = config['BASE_SURVEY_URL'] + base_path
        url_builder_params = config['URL_BUILDER_PARAMS']
        
        # Add parameters to URL (optimized with list comprehension)
        param_list = [
            f"{param_name}={url_builder_params[param_name]}"
            for param_name, include in parameters.items()
            if include and param_name in url_builder_params
        ]
        
        if param_list:
            separator = "&" if "?" in url else "?"
            url += separator + "&".join(param_list)
        
        return url


class FileHandler:
    """Handles file operations."""
    
    @staticmethod
    def ensure_directory_exists(directory_path: str) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory_path: Path to the directory
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """
        Convert a string to a safe filename by removing/replacing invalid characters.
        
        Args:
            filename: Original filename
            
        Returns:
            Safe filename
        """
        # Replace invalid characters with underscores
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove leading/trailing spaces and dots
        safe_name = safe_name.strip('. ')
        return safe_name 