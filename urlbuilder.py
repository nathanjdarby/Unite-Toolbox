import tkinter as tk 
from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import webbrowser
import pyperclip
import subprocess
import sys
import os

# Function to build the URL
def build_url():

    global url

    base_url = "https://surveys.unitetheunion.org/"

    user_input = entry.get()

    url = base_url + user_input

    open_browser_button.config(state="normal")

    if var1.get():

        if "?" not in url:

            url += "?FirstName=(|MM_FirstName|)"

        else:

            url += "&FirstName=(|MM_FirstName|)"

    if var2.get():

        if "?" not in url:

            url += "?LastName=(|MM_LastName|)"

        else:

            url += "&LastName=(|MM_LastName|)"

    if var3.get():

        if "?" not in url:

            url += "?MembershipNumber=(|MembershipNumber|)"

        else:

            url += "&MembershipNumber=(|MembershipNumber|)"

    if var4.get():

        if "?" not in url:

            url += "?MobilePhone=(|MobilePhone|)"

        else:

            url += "&MobilePhone=(|MobilePhone|)"

    if var5.get():

        if "?" not in url:

            url += "?EmailAddress=(|MM_EmailAddress|)"

        else:

            url += "&EmailAddress=(|MM_EmailAddress|)"

    if var6.get():

        if "?" not in url:

            url += "?EmployerName=(|MM_EmployerName|)"

        else:

            url += "&EmployerName=(|MM_EmployerName|)"

    if var7.get():

        if "?" not in url:

            url += "?WorkplaceName=(|WorkplaceName|)"

        else:

            url += "&WorkplaceName=(|WorkplaceName|)"

    if var8.get():

        if "?" not in url:

            url += "?JobTitle=(|JobTitle|)"

        else:

            url += "&JobTitle=(|JobTitle|)"

    if var9.get():

        if "?" not in url:

            url += "?WorkplaceCode=(|MM_WorkplaceCode|)"

        else:

            url += "&WorkplaceCode=(|MM_WorkplaceCode|)"

    if var10.get():

        if "?" not in url:

            url += "?JobCode=(|MM_JobCode|)"

        else:

            url += "&JobCode=(|MM_JobCode|)"

    if var11.get():

        if "?" not in url:

            url += "?EmployerCode=(|EmployerCode|)"

        else:

            url += "&EmployerCode=(|EmployerCode|)"

    if var12.get():

        if "?" not in url:

            url += "?HomeAddress[addr_line1]=(|MM_HomeAddress1|)"

        else:

            url += "&HomeAddress[addr_line1]=(|MM_HomeAddress1|)"

    if var13.get():

        if "?" not in url:

            url += "?HomeAddress[addr_line2]=(|MM_HomeAddress2|)"

        else:

            url += "&HomeAddress[addr_line2]=(|MM_HomeAddress2|)"

    if var14.get():

        if "?" not in url:

            url += "?HomeAddress[postal]=(|MM_HomeAddressPostcode|)"

        else:

            url += "&HomeAddress[postal]=(|MM_HomeAddressPostcode|)"

    if var15.get():

        if "?" not in url:

            url += "?WorkplaceAddress[addr_line1]=(|MM_WorkplaceAddress1|)"

        else:

            url += "&WorkplaceAddress[addr_line1]=(|MM_WorkplaceAddress1|)"

    if var16.get():

        if "?" not in url:

            url += "?WorkplaceAddress[addr_line2]=(|MM_WorkplaceAddress2|)"

        else:

            url += "&WorkplaceAddress[addr_line2]=(|MM_WorkplaceAddress2|)"

    if var17.get():

        if "?" not in url:

            url += "?WorkplaceAddress[postal]=(|MM_WorkplaceAddressPostcode|)"

        else:

            url += "&WorkplaceAddress[postal]=(|MM_WorkplaceAddressPostcode|)"

    pyperclip.copy(url)

    messagebox.showinfo(
        "URL Copied", "The URL has been copied to the clipboard.")

    print(url)

# Opens the browser with the URL
def open_browser():

    browser = webbrowser.get()

    browser.open_new_tab(url)

# Resets the checkboxs
def reset_checkboxes():

    for i in range(1, 18):

        var = eval(f"var{i}")

        var.set(False)

def test_id():
    entry.delete(0, tk.END)
    entry.insert(0, "223464332740956")

root = tk.Tk()

# Application Settings
root.geometry("500x330")
root.title("Mass Mailer URL Builder")

# URL BUILDER 
label = tk.Label(root, text="Enter your Survey ID:")
label.grid(column=0, row=0, sticky="w", padx=5, pady=5)

# SURVEY ID Input
entry = tk.Entry(root)
entry.grid(column=1, row=0, sticky="w", padx=5, pady=5)

# URL Variables
var1 = tk.IntVar() 
check1 = tk.Checkbutton(root, text="First Name", variable=var1)
check1.grid(column=0, row=1, sticky="w")

var2 = tk.IntVar()
check2 = tk.Checkbutton(root, text="Last Name", variable=var2)
check2.grid(column=1, row=1, sticky="w")

var3 = tk.IntVar()
check3 = tk.Checkbutton(root, text="Membership Number", variable=var3)
check3.grid(column=1, row=2, sticky="w")

var4 = tk.IntVar()
check4 = tk.Checkbutton(root, text="Mobile Phone", variable=var4)
check4.grid(column=0, row=3, sticky="w")

var5 = tk.IntVar()
check5 = tk.Checkbutton(root, text="Email Address", variable=var5)
check5.grid(column=0, row=2, sticky="w")

var6 = tk.IntVar()
check6 = tk.Checkbutton(root, text="Employer Name", variable=var6)
check6.grid(column=1, row=3, sticky="w")

var7 = tk.IntVar()
check7 = tk.Checkbutton(root, text="Workplace Name", variable=var7)
check7.grid(column=0, row=4, sticky="w")

var8 = tk.IntVar()
check8 = tk.Checkbutton(root, text="Job Title", variable=var8)
check8.grid(column=1, row=4, sticky="w")

var9 = tk.IntVar()
check9 = tk.Checkbutton(root, text="Workplace Code", variable=var9)
check9.grid(column=0, row=5, sticky="w")

var10 = tk.IntVar()
check10 = tk.Checkbutton(root, text="Job Code", variable=var10)
check10.grid(column=1, row=5, sticky="w")

var11 = tk.IntVar()
check11 = tk.Checkbutton(root, text="Employer Code", variable=var11)
check11.grid(column=0, row=6, sticky="w")

var12 = tk.IntVar()
check12 = tk.Checkbutton(root, text="Home Address 1", variable=var12)
check12.grid(column=1, row=6, sticky="w")

var13 = tk.IntVar()
check13 = tk.Checkbutton(root, text="Home Address 2", variable=var13)
check13.grid(column=0, row=7, sticky="w")

var14 = tk.IntVar()
check14 = tk.Checkbutton(root, text="Home Postcode", variable=var14)
check14.grid(column=1, row=7, sticky="w")

var15 = tk.IntVar()
check15 = tk.Checkbutton(root, text="Workplace Address 1", variable=var15)
check15.grid(column=0, row=8, sticky="w")

var16 = tk.IntVar()
check16 = tk.Checkbutton(root, text="Workplace Address 2", variable=var16)
check16.grid(column=1, row=8, sticky="w")

var17 = tk.IntVar()
check17 = tk.Checkbutton(root, text="Workplace Postcode", variable=var17)
check17.grid(column=0, row=9, sticky="w")

# A button to build the URL generated by the users choices
button = tk.Button(root, text="Build URL", command=build_url)
button.grid(column=0, row=12, sticky="w", padx=5, pady=5)

# Opens up a broswer with the newly created URL
open_browser_button = tk.Button(
    root, text="Open URL in browser", command=open_browser, state="disabled"
)
open_browser_button.grid(column=1, row=12, sticky="w", padx=5, pady=5)

# Creates a button to reset the checkboxes
reset_button = tk.Button(root, text="Reset", command=reset_checkboxes)
reset_button.grid(column=2, row=12, sticky="w", padx=5, pady=5)

# Adds a Test Survey ID to the Inputcl
test_id_button = tk.Button(root, text="Test ID", command=test_id)
test_id_button.grid(column=0, row=13, sticky="w", padx=5, pady=5)

root.mainloop()