import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext, Listbox, END, messagebox
import re 
from tkhtmlview import HTMLLabel


# Function to fetch HTML content from the given URL
def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        return None

# Function to analyze the input element and return validation results
def analyze_input(input_element):
    result = []
    classes = input_element.get('class', [])
    
    # Check various attributes and append the results
    has_form_readonly = 'form-readonly' in classes
    result.append(('Read Only: ', "Yes" if has_form_readonly else "No"))
    
    has_validate_required = 'validate[required]' in classes
    result.append(('Required: ', "Yes" if has_validate_required else "No"))
    
    name_attribute = input_element.get('name', '')
    has_membership_number = name_attribute.endswith("MembershipNumber")
    result.append(('Unique Name is "MembershipNumber": ', "Yes" if has_membership_number else "No"))
    
    # Include the actual name if it doesn't end with "MembershipNumber"
    if not has_membership_number:
        result.append(('Unique Name is: ', name_attribute))

    return result

# Main application function
def main():
    # Create the main window
    root = tk.Tk()
    root.title("JotForm Validator")

    # Initialize global variables
    soup = None

    # Function to start the web scraping process
    def start_scraping():
        nonlocal soup
        url = url_entry.get()
        html_data = get_website_data(url)
        
        # Process the HTML content if successfully fetched
        if html_data:
            soup = BeautifulSoup(html_data, 'html.parser')
            
            # Find and display the title from the "form-header" class
            form_header = soup.find(class_="form-header")
            if form_header:
                form_title = form_header.get_text(strip=True)
                form_title_label.config(text=form_title)
            else:
                form_title_label.config(text="Form Title Not Found")

            # Update the labels listbox with all labels found in the HTML
            labels = soup.find_all('label')
            labels_listbox.delete(0, END)
            for label in labels:
                labels_listbox.insert(END, label.text.strip())

    # Function to handle validation of selected label
    def scrape_selected_label():
        nonlocal soup
        selection = labels_listbox.curselection()
        if selection and soup:
            selected_text = labels_listbox.get(selection[0]).strip()
            normalized_selected_text = selected_text.rstrip('*').strip()

            # Find the label by normalized text
            label = soup.find(lambda tag: tag.name == "label" and 
                              normalized_selected_text in tag.get_text(strip=True))

            if label and label.has_attr('for'):
                input_element = soup.find('input', id=label['for'])
                if input_element:
                    # Analyze the input element and display the results
                    results = analyze_input(input_element)
                    output_text.config(state=tk.NORMAL)
                    output_text.delete('1.0', tk.END)
                    for text, value in results:
                        output_text.insert(tk.END, text + value + '\n', 'red' if value == "No" else 'black')
                    output_text.tag_config('red', foreground='red')
                    output_text.config(state=tk.DISABLED)
                else:
                    messagebox.showerror("Error", "Associated input not found.")
            else:
                messagebox.showerror("Error", "Label not found.")

    # Build the GUI components
    tk.Label(root, text="Enter JotForm URL:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    url_entry = tk.Entry(root)
    url_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    url_entry.focus_set()

    scrape_button = tk.Button(root, text="Search", command=start_scraping)
    scrape_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    form_title_label = tk.Label(root, text="Form Title", font=('TkDefaultFont', 24))
    form_title_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    tk.Label(root, text="Labels:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    labels_listbox = Listbox(root)
    labels_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrape_label_button = tk.Button(root, text="Validate", command=scrape_selected_label)
    scrape_label_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    tk.Label(root, text="Validated Data:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    output_text = scrolledtext.ScrolledText(root, height=10, font=('TkDefaultFont', 22))
    output_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Start the Tkinter event loop
    root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    main()
