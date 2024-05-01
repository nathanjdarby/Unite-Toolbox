import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox



def select_file(title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=[("CSV files", "*.csv")])
    return file_path

def input_dialog(prompt):
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring("Input", prompt)
    return user_input

def alert(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Alert", message)

def save_file_location(default_path):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", initialdir=default_path, title="Save As", filetypes=[("CSV files", "*.csv")])
    return file_path

# Prompt the user to select the CSV files
file1 = select_file("Select the first CSV file")
file2 = select_file("Select the second CSV file")

# Prompt the user to enter the membership column name
membership_column = input_dialog("Please enter the name of the membership column:")

# Read the CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Check if both CSV files have the specified column
if membership_column not in df1.columns or membership_column not in df2.columns:
    alert(f"The specified membership column '{membership_column}' is not present in one or both CSV files.")
    exit()

# Merge the two CSV files on the specified column, marking differences
merged_df = pd.merge(df1, df2, on=membership_column, how='outer', indicator=True)

# Filter the merged DataFrame to find rows that exist in file1 but not in file2
missing_rows = merged_df[merged_df['_merge'] == 'left_only']

# Drop the merge indicator column
missing_rows = missing_rows.drop(columns=['_merge'])

# If missing rows were found, save them to a new CSV file
if not missing_rows.empty:
    default_save_path = "CompareResults"
    if not os.path.exists(default_save_path):
        os.makedirs(default_save_path)
    save_path = save_file_location(default_save_path)
    missing_rows.to_csv(save_path, index=False)
    alert(f"Missing rows have been saved to '{save_path}'.")
else:
    alert('No missing rows found.')
