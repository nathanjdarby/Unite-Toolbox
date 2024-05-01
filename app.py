import tkinter as tk 
from tkinter import filedialog, messagebox
import pandas as pd
import webbrowser
import subprocess
import os
import re
from premailer import transform
import pyperclip

# Predefined list of JotForm templates
websites = {
    "Annonymous/Feedback Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/anonymous-feedback-form-template",
    "CAC Petition Form": "https://surveys.unitetheunion.org/form-templates/ur/cac-union-recognition-petition-template",
    "Collective Grievance": "https://surveys.unitetheunion.org/form-templates/ur/collective-grievance-template",
    "Consultative Ballot": "https://surveys.unitetheunion.org/form-templates/standalone/ur/standard-consultative-ballot-template",
    "Event Booking Form:": "https://surveys.unitetheunion.org/form-templates/standalone/ur/event-booking-form-template",
    "Generic Data Cleanse Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/generic-data-cleansing-form-non-industrial-action-template",
    "Generic Organiser Survey": "https://surveys.unitetheunion.org/form-templates/standalone/ur/generic-organiser-survey-form-template",
    "Industrial Action - Data Cleanse": "https://surveys.unitetheunion.org/form-templates/standalone/ur/industrial-action-data-cleansing-form-template",
    "Rep Election Ballot": "https://surveys.unitetheunion.org/form-templates/ur/unite-rep-ballot",
    "Strike Pay Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/strike-pay-form"
}

# Function to launch the validator app
def launch_other_app():
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Filename of the other Python script
    other_app_filename = 'validate-jot.py'
    # Full path to the other Python script
    other_app_path = os.path.join(dir_path, other_app_filename)
    # Launch the other application
    subprocess.Popen(['python3', other_app_path])

# Function to remove unwanted columns from CSV
def remove_columns():
    global df
    # Define the columns to keep and the new column names
    columns_to_keep = ["First Name", "Surname", "Member Number", "Address - Home - Line 1",
                       "Address - Home - Line 2", "Address - Home - Line 3",
                       "Address - Home - Line 4", "Address - Home PC", "Employer Name",
                       "Employer", "Workplace Name", "Workplace", "Region",
                       "Job Description ", "Email Address", "Allow Email", "Allow Phone",
                       "Allow SMS", "Home phone", "Mobile phone", "TPS Flag"]
    new_column_names = {"First Name": "FirstName", "Surname": "LastName", "Member Number": "MembershipNumber",
                        "Address - Home - Line 1": "HomeAddress1", "Address - Home - Line 2": "HomeAddress2",
                        "Address - Home - Line 3": "HomeAddress3", "Address - Home - Line 4": "HomeAddress4",
                        "Address - Home PC": "HomeAddressPostcode", "Employer Name": "EmployerName",
                        "Employer": "EmployerCode", "Workplace Name": "WorkplaceName", "Workplace": "WorkplaceCode",
                        "Region": "Region", "Job Description ": "JobTitle", "Email Address": "EmailAddress",
                        "Allow Email": "AllowEmail", "Allow Phone": "AllowPhone", "Allow SMS": "AllowSms",
                        "Home phone": "HomePhone", "Mobile phone": "MobilePhone", "TPS Flag": "TPS"}
    # Remove all other columns and rename the remaining ones
    df = df[columns_to_keep]
    df = df.rename(columns=new_column_names)

# Function to select and process CSV file
def select_file():
    global df
    # Create a root window
    root = tk.Tk()
    root.withdraw()
    # Open a file dialog to select CSV file
    filepath = filedialog.askopenfilename()
    # Read the selected file into a DataFrame
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=root)
        return
    expected_headers = ["First Name", "Surname", "Member Number", "Address - Home - Line 1",
                   "Address - Home - Line 2", "Address - Home - Line 3",
                   "Address - Home - Line 4", "Address - Home PC", "Employer Name",
                   "Employer", "Workplace Name", "Workplace", "Region",
                   "Job Description ", "Email Address", "Allow Email", "Allow Phone",
                   "Allow SMS", "Home phone", "Mobile phone", "TPS Flag"]
    missing_headers = set(expected_headers) - set(df.columns)
    if len(missing_headers) > 0:
        messagebox.showerror("Missing Headers", f"The file selected is missing the following headers: {', '.join(missing_headers)}", parent=root)
        return
    # Remove unwanted columns
    remove_columns()
    # Open a file dialog to select save location
    filepath = filedialog.asksaveasfilename(defaultextension=".csv")
    # Save the DataFrame to the selected location
    df.to_csv(filepath, index=False)
    # Inform the user about the saved file
    messagebox.showinfo("File Selected", f"The file '{filepath}' has been converted and saved.", parent=root)

# Function to divide CSV file by Workplace
def workplacedivide():
    # Prompt the user to select the input file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

    # Load the file into a pandas dataframe
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("File type not supported")

    # Get the unique values in the "workplace_name" column
    unique_codes = df["Workplace Name"].unique()

    # Ask the user where to save the new files
    save_path = filedialog.askdirectory()

    # Iterate through the unique code names and create a new dataframe
    # for each one that contains all rows with that code name
    for code in unique_codes:
        code_df = df[df["Workplace Name"] == code]
        # Save the new dataframe in a file with the unique code name as the file name
        file_name = f"{code}.xlsx" if file_path.endswith('.xlsx') else f"{code}.csv"
        code_df.to_excel(os.path.join(save_path, file_name), index=False) if file_path.endswith('.xlsx') else code_df.to_csv(os.path.join(save_path, file_name), index=False)

# Function to process CSV file into an SMS list
def SMS_only():
     # Prompt the user to select the input file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])

    # Load the file into a pandas dataframe
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("File type not supported")
    
    # Makes all columns lower case to deal with case sensitivity
    df.columns = df.columns.str.lower()
    
    # Add any "Home phone" rows starting with "07" or "7" to "Mobile phone"
    df.loc[df["home phone"].notna() & df["home phone"].str.startswith(("07", "7")), "mobile phone"] = df["home phone"]

    # Keep rows where "Allow SMS" is "Y"
    df = df.loc[df["allow sms"] == "Y"]

    # Remove empty rows from the "Mobile phone" column
    df = df.dropna(subset=["mobile phone"])

    # Keep only the "Allow SMS" and "Mobile phone" columns
    df = df[["member number", "first name", "surname","allow sms", "mobile phone"]]

    # Prompt the user to select where to save the modified file
    save_path = filedialog.asksaveasfilename(defaultextension=".csv")

    # Save the modified dataframe to the selected file path
    df.to_csv(save_path, index=False)

    # Open the saved file
    os.system(f'open "{save_path}"')

    # Print a message to indicate the file has been saved and opened
    print(f"File saved and opened: {save_path}")

# Function to open URL in web browser
def open_url():
    selected_site_name = site_name_var.get()
    selected_url = websites[selected_site_name]
    webbrowser.open(selected_url)

# Remove the style tag from HTML content
def remove_style_tag(html_content):
    return re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)

# Function to remove MSO code and inline CSS in HTML content
def remove_mso_code(html_content):
    mso_regex = r'<!--\[if.*?\[endif\]-->'
    return re.sub(mso_regex, '', html_content, flags=re.DOTALL)

# Function to inline CSS in HTML content
def inline_css(html_content):
    return transform(html_content)

# Function to process HTML file by removing style tag and inlining CSS
def process_html_file(html_content):
    html_without_mso = remove_mso_code(html_content)
    html_inlined_css = inline_css(html_without_mso)
    return html_inlined_css

# Function to handle HTML file processing
def handle_html_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
            processed_html = process_html_file(html_content)
            save_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
            if save_path:
                with open(save_path, 'w', encoding='utf-8') as file:
                    file.write(processed_html)
                pyperclip.copy(processed_html)  # Save processed HTML to clipboard
                messagebox.showinfo("Success", "HTML processed successfully and copied to clipboard!", parent=root)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}", parent=root)

# APPLICATION GUI

# Application Root
root = tk.Tk()

# Application Settings
root.geometry("800x150")
root.title("Unite Ballot Toolbox")
root.attributes("-topmost", True)

# create a menu bar
menu_bar = tk.Menu(root)
links_menu = tk.Menu(menu_bar, tearoff=0)
links_menu.add_command(label="Validator", command=launch_other_app)
links_menu.add_command(label="---------------")
menu_bar.add_cascade(label="Jotform", menu=links_menu)

# Add JotForm Templates submenu
jotform_templates_menu = tk.Menu(links_menu, tearoff=0)
for site_name, site_url in websites.items():
    jotform_templates_menu.add_command(label=site_name, command=lambda url=site_url: webbrowser.open(url))
links_menu.add_cascade(label="JotForm Templates", menu=jotform_templates_menu)

root.config(menu=menu_bar)

# CSV Labels
csv_label = tk.Label(root, text="CSV Tools")
csv_label.grid(column=0, row=1, sticky="w", padx=5, pady=5)

# CSV Tools Buttons
uwp_to_csv = tk.Button(root, text="CSV 2 UWP", command=select_file)
uwp_to_csv.grid(column=0, row=2, sticky="w", padx=5, pady=5)

sms_to_csv = tk.Button(root, text="CSV 2 SMS List", command=SMS_only)
sms_to_csv.grid(column=1, row=2, sticky="w", padx=5, pady=5)

csv_to_workplacedivide = tk.Button(root, text="CSV Divide by Workplace", command=workplacedivide)
csv_to_workplacedivide.grid(column=2, row=2, sticky="w", padx=5, pady=5)


# Button to process HTML file
html_to_css_button = tk.Button(root, text="Process HTML File", command=handle_html_file)
html_to_css_button.grid(column=0, row=3, sticky="w", padx=5, pady=5)

root.mainloop()
