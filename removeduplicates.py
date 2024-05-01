import csv

# Read the numbers from the "respond.csv" file
numbers_to_remove = []
with open('respond.csv', 'r') as respond_file:
    respond_reader = csv.reader(respond_file)
    for row in respond_reader:
        numbers_to_remove.append(row[0])  # Assuming numbers are in the first column

# Remove matching rows from "smsdata.csv" and create a new file "smsdata_filtered.csv"
with open('smsdata.csv', 'r') as smsdata_file, \
        open('smsdata_filtered.csv', 'w', newline='') as filtered_file:
    smsdata_reader = csv.reader(smsdata_file)
    filtered_writer = csv.writer(filtered_file)
    header = next(smsdata_reader)  # Read the header
    filtered_writer.writerow(header)  # Write the header to the new file
    
    for row in smsdata_reader:
        if row[0] not in numbers_to_remove:  # Assuming membership_number is in the first column
            filtered_writer.writerow(row)  # Write the row to the new file if it doesn't match

print("Filtering completed. The filtered data is stored in 'smsdata_filtered.csv'.")
