import json
import os

# Define the file paths
bulk_input_file = 'bulk_input.txt'  # File for uploading data
safeum_file = 'safeum.json'  # File to store data

# Check if the safeum.json file exists, if not create an empty one
if not os.path.exists(safeum_file):
    with open(safeum_file, 'w') as f:
        json.dump({}, f)

# Function to load data from the safeum.json file
def load_data():
    with open(safeum_file, 'r') as f:
        return json.load(f)

# Function to save data to the safeum.json file
def save_data(data):
    with open(safeum_file, 'w') as f:
        json.dump(data, f, indent=4)

# Function to display stored account info
def display_account_info():
    data = load_data()
    if not data:
        print("No account info stored.")
    else:
        for username, phone in data.items():
            print(f"Username: {username}, Phone Number: {phone}")

# Function to upload bulk data from the bulk_input.txt file
def upload_bulk_data():
    # Check if the bulk_input.txt file exists
    if not os.path.exists(bulk_input_file):
        print(f"{bulk_input_file} not found, please create this file with the data.")
        return

    data = load_data()

    # Read the bulk_input.txt file and update the account info
    with open(bulk_input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '@' in line:
                username, phone = line.split('@', 1)
                data[username] = phone
            else:
                print(f"Skipping invalid line: {line}")

    save_data(data)
    print(f"Bulk data from {bulk_input_file} has been uploaded successfully!")

# Function to search by phone number(s)
def search_by_phone():
    data = load_data()
    
    # Ask user for phone numbers
    phone_numbers_input = input("Enter phone numbers separated by commas: ").strip()
    phone_numbers = [phone.strip() for phone in phone_numbers_input.split(',')]

    found = False
    for phone_number in phone_numbers:
        # Search for the phone number in the data
        for username, phone in data.items():
            if phone == phone_number:
                print(f"Phone number {phone_number} is associated with username: {username}")
                found = True
                break
        if not found:
            print(f"No account found for phone number {phone_number}")

# Main function to display menu
def main():
    while True:
        print("\nSafeum Account Info")
        print("1. Display Account Info")
        print("2. Upload Bulk Account Info (from bulk_input.txt)")
        print("3. Search by Phone Number")
        print("4. Exit")
        choice = input("Choose an option (1/2/3/4): ")

        if choice == '1':
            display_account_info()
        elif choice == '2':
            upload_bulk_data()
        elif choice == '3':
            search_by_phone()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    # Create the bulk_input.txt file if it doesn't exist
    if not os.path.exists(bulk_input_file):
        with open(bulk_input_file, 'w') as f:
            f.write("lfc19wplxzgxo9ct1@994409446723\n")  # Example entry
            f.write("iicr330taa7kj7pml@994405909121\n")  # Example entry
            f.write("awvrd9ep3r6nm1dts@994408701494\n")  # Example entry
            print(f"{bulk_input_file} created. Add your account data in this file.")

    # Start the main program
    main()
