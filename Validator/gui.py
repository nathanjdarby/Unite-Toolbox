import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

# Function to send a GET request to the website
def get_website_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.text
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Request failed: {e}")
        return None

# Function to analyze the soup object
def analyze_soup(soup):
    # Initialize result string
    result = ""

    # Find all label tags in the HTML
    labels = soup.find_all('label')

    # Check if any label contains the text "Membership Number"
    membership_label_exists = any("Membership Number" in label.text for label in labels)
    result += f'Label with the text "Membership Number" found: {membership_label_exists}\n'

    # Additional scraping logic...
    # Find the label that contains the text "Membership Number"
    label = soup.find(lambda tag: tag.name == "label" and "Membership Number" in tag.text)
    
    # Initialize variables to keep track of the classes and name presence
    has_form_readonly = False
    has_validate_required = False
    has_membership_number_at_end = False

    # If the label is found, find the associated input element by its id
    if label:
        input_id = label.get('for')
        input_element = soup.find('input', id=input_id)

        # Check if the input element has the class "form-readonly"
        if input_element:
            classes = input_element.get('class', [])
            has_form_readonly = 'form-readonly' in classes
            has_validate_required = 'validate[required]' in classes
            
            # Check if the 'name' attribute ends with "MembershipNumber"
            name_attribute = input_element.get('name', '')
            if name_attribute.endswith("MembershipNumber"):
                has_membership_number_at_end = True
            else:
                has_membership_number_at_end = False

    # Construct the results
    result += f'Input with "form-readonly" class present: {has_form_readonly}\n'
    result += f'Input with "validate[required]" class present: {has_validate_required}\n'
    result += f'Input name ends with "MembershipNumber": {has_membership_number_at_end}\n'
    if not has_membership_number_at_end and input_element:
        result += f'The unique name is: {input_element.get("name")}\n'
    else:
        result += 'The unique name is not applicable or input not found.\n'

    return result

def main():
    # Create the main window
    root = tk.Tk()
    root.title("JotForm Ballot Validator")

    # Function to handle the scraping when button is clicked
    def start_scraping():
        url = url_entry.get()  # Get the URL from the entry widget
        html_data = get_website_data(url)
        if html_data:
            soup = BeautifulSoup(html_data, 'html.parser')
            
            # Find all labels and list them
            labels = soup.find_all('label')
            all_labels = '\n'.join(label.text.strip() for label in labels)

            # Output all labels to the labels text area
            labels_text.config(state=tk.NORMAL)
            labels_text.delete('1.0', tk.END)
            labels_text.insert(tk.END, all_labels)
            labels_text.config(state=tk.DISABLED)

            # Now analyze the soup for detailed scraped data
            result = analyze_soup(soup)

            # Output the detailed results to the output text area
            output_text.config(state=tk.NORMAL)
            output_text.delete('1.0', tk.END)
            output_text.insert(tk.END, result)
            output_text.config(state=tk.DISABLED)

    # URL entry
    tk.Label(root, text="Enter URL:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    url_entry = tk.Entry(root)
    url_entry.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    url_entry.focus_set()

    # Scrape button
    scrape_button = tk.Button(root, text="Scrape", command=start_scraping)
    scrape_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

    # Scrolling text area to display all labels
    tk.Label(root, text="All Labels:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    labels_text = scrolledtext.ScrolledText(root, height=10)
    labels_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Scrolling text area to display scraped data
    tk.Label(root, text="Scraped Data:").pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    output_text = scrolledtext.ScrolledText(root, height=10)
    output_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Run the main loop
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
