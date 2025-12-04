"""
Configuration file for Unite Toolbox application.
Contains all constants, settings, and data mappings used across the application.
"""

# JotForm template URLs
JOTFORM_TEMPLATES = {
    "Anonymous/Feedback Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/anonymous-feedback-form-template",
    "CAC Petition Form": "https://surveys.unitetheunion.org/form-templates/ur/cac-union-recognition-petition-template",
    "Collective Grievance": "https://surveys.unitetheunion.org/form-templates/ur/collective-grievance-template",
    "Consultative Ballot": "https://surveys.unitetheunion.org/form-templates/standalone/ur/standard-consultative-ballot-template",
    "Event Booking Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/event-booking-form-template",
    "Generic Data Cleanse Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/generic-data-cleansing-form-non-industrial-action-template",
    "Generic Organiser Survey": "https://surveys.unitetheunion.org/form-templates/standalone/ur/generic-organiser-survey-form-template",
    "Industrial Action - Data Cleanse": "https://surveys.unitetheunion.org/form-templates/standalone/ur/industrial-action-data-cleansing-form-template",
    "Rep Election Ballot": "https://surveys.unitetheunion.org/form-templates/ur/unite-rep-ballot",
    "Strike Pay Form": "https://surveys.unitetheunion.org/form-templates/standalone/ur/strike-pay-form"
}

# CSV column mappings for UWP conversion
CSV_COLUMN_MAPPING = {
    "columns_to_keep": [
        "First Name", "Surname", "Member Number", "Address - Home - Line 1",
        "Address - Home - Line 2", "Address - Home - Line 3",
        "Address - Home - Line 4", "Postcode", "Name",
        "Employer", "Workplace Name", "Workplace", "Region",
        "Job Description", "Email Address", "Allow Email", "Allow Phone",
        "Allow SMS", "Home phone", "Mobile phone", "TPS Flag"
    ],
    "new_column_names": {
        "First Name": "FirstName",
        "Surname": "LastName", 
        "Member Number": "MembershipNumber",
        "Address - Home - Line 1": "HomeAddress1",
        "Address - Home - Line 2": "HomeAddress2",
        "Address - Home - Line 3": "HomeAddress3",
        "Address - Home - Line 4": "HomeAddress4",
        "Postcode": "HomeAddressPostcode",
        "Name": "EmployerName",
        "Employer": "EmployerCode",
        "Workplace Name": "WorkplaceName",
        "Workplace": "WorkplaceCode",
        "Region": "Region",
        "Job Description": "JobTitle",
        "Email Address": "EmailAddress",
        "Allow Email": "AllowEmail",
        "Allow Phone": "AllowPhone",
        "Allow SMS": "AllowSms",
        "Home phone": "HomePhone",
        "Mobile phone": "MobilePhone",
        "TPS Flag": "TPS"
    }
}

# URL builder parameters
URL_BUILDER_PARAMS = {
    "FirstName": "(|MM_FirstName|)",
    "LastName": "(|MM_LastName|)",
    "MembershipNumber": "(|MembershipNumber|)",
    "MobilePhone": "(|MobilePhone|)",
    "EmailAddress": "(|MM_EmailAddress|)",
    "EmployerName": "(|MM_EmployerName|)",
    "WorkplaceName": "(|WorkplaceName|)",
    "JobTitle": "(|JobTitle|)",
    "WorkplaceCode": "(|MM_WorkplaceCode|)",
    "JobCode": "(|MM_JobCode|)",
    "EmployerCode": "(|EmployerCode|)",
    "HomeAddress[addr_line1]": "(|MM_HomeAddress1|)",
    "HomeAddress[addr_line2]": "(|MM_HomeAddress2|)",
    "HomeAddress[postal]": "(|MM_HomeAddressPostcode|)",
    "WorkplaceAddress[addr_line1]": "(|MM_WorkplaceAddress1|)",
    "WorkplaceAddress[addr_line2]": "(|MM_WorkplaceAddress2|)",
    "WorkplaceAddress[postal]": "(|MM_WorkplaceAddressPostcode|)"
}

# Application settings
APP_SETTINGS = {
    "title": "Unite Ballot Toolbox",
    "geometry": "800x250",
    "topmost": True
}

# File types
SUPPORTED_FILE_TYPES = {
    "csv": [("CSV files", "*.csv")],
    "excel": [("Excel files", "*.xlsx")],
    "html": [("HTML files", "*.html")],
    "all_data": [("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
}

# Base URL for surveys
BASE_SURVEY_URL = "https://surveys.unitetheunion.org/" 