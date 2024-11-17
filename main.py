import json
import os
import platform
import pyfiglet
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Define the file paths
bulk_input_file = 'bulk_input.txt'  # File for uploading data
safeum_file = 'safeum.json'  # File to store data

# Function to clear the terminal screen
def clear_screen():
    # Check the operating system and execute the appropriate command to clear the screen
    system_name = platform.system().lower()
    
    if system_name == 'windows':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux/Termux/macOS

# Function to display the banner
def display_banner():
    banner = pyfiglet.Figlet(font="small")
    banner_text = banner.renderText("DARK DEVIL")
    
    terminal_width = os.get_terminal_size().columns
    centered_banner = '\n'.join(line.center(terminal_width) for line in banner_text.splitlines())
    
    print(Fore.CYAN + centered_banner)
    author_line = f"{Fore.YELLOW}Author/Github: {Style.RESET_ALL}{Fore.GREEN}@AbdurRehman1129"
    print(author_line.center(terminal_width))

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
        print(Fore.RED + "No account info stored.")
    else:
        for username, phone in data.items():
            print(f"{Fore.GREEN}Username: {Style.RESET_ALL}{username} {Fore.YELLOW}Phone Number: {Style.RESET_ALL}{phone}")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to upload bulk data from the bulk_input.txt file
def upload_bulk_data():
    # Check if the bulk_input.txt file exists
    if not os.path.exists(bulk_input_file):
        print(Fore.RED + f"{bulk_input_file} not found, please create this file with the data.")
        input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue
        return

    data = load_data()

    # Read the bulk_input.txt file and update the account info
    with open(bulk_input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '@' in line:
                username, phone = line.split('@', 1)
                data[username] = phone.replace(" ", "")  # Remove spaces from phone numbers
            else:
                print(Fore.RED + f"Skipping invalid line: {line}")

    save_data(data)
    print(Fore.GREEN + f"Bulk data from {bulk_input_file} has been uploaded successfully!")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to search by phone number(s)
def search_by_phone():
    data = load_data()
    
    # Ask user for phone numbers
    phone_numbers_input = input(Fore.YELLOW + "Enter phone numbers separated by commas: ").strip()
    phone_numbers = [phone.strip().replace(" ", "") for phone in phone_numbers_input.split(',')]

    found = False
    for phone_number in phone_numbers:
        # Search for the phone number in the data
        for username, phone in data.items():
            if phone == phone_number:
                print(f"{Fore.GREEN}Phone number {phone_number} is associated with username: {Style.RESET_ALL}{username}")
                found = True
                break
        if not found:
            print(Fore.RED + f"No account found for phone number {phone_number}")
    
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to remove account data (by username or phone number)
def remove_data():
    data = load_data()
    
    # Ask user for username or phone number to remove
    remove_input = input(Fore.YELLOW + "Enter Username or Phone Number to remove: ").strip()
    
    # Find and remove the account by username
    if remove_input in data:
        del data[remove_input]
        save_data(data)
        print(Fore.GREEN + f"Account with username/phone number {remove_input} has been removed.")
    else:
        # Check if any phone number matches
        found = False
        for username, phone in data.items():
            if phone == remove_input:
                del data[username]  # Remove account by username if phone number matches
                save_data(data)
                print(Fore.GREEN + f"Account with phone number {remove_input} has been removed.")
                found = True
                break
        if not found:
            print(Fore.RED + "No account found with the provided username/phone number.")
    
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to manually enter username and phone number
def manual_entry():
    data = load_data()
    
    while True:
        username = input(Fore.YELLOW + "Enter Username: ").strip()
        phone = input(Fore.YELLOW + "Enter Phone Number (with no spaces): ").strip().replace(" ", "")
        
        # Check if username or phone number already exists
        if username in data:
            print(Fore.RED + f"Username {username} already exists.")
        elif phone in data.values():
            print(Fore.RED + f"Phone number {phone} already exists.")
        else:
            # Save the new data
            data[username] = phone
            save_data(data)
            print(Fore.GREEN + "Account info added successfully!")
        
        # Ask if user wants to add another entry
        continue_input = input(Fore.YELLOW + "Do you want to enter another account? (Y/N): ").strip().lower()
        if continue_input != 'y':
            break

# Main function to display menu
def main():
    while True:
        clear_screen()  # Clear screen at the beginning of each run
        display_banner()  # Display the banner
        print(Fore.GREEN + "Safeum Account Info")
        print(Fore.GREEN + "1. Display Account Info")
        print(Fore.GREEN + "2. Upload Bulk Account Info (from bulk_input.txt)")
        print(Fore.GREEN + "3. Search by Phone Number")
        print(Fore.GREEN + "4. Manually Enter Account Info")
        print(Fore.GREEN + "5. Remove Account Info")
        print(Fore.GREEN + "6. Exit")
        
        try:
            choice = input(Fore.WHITE + "Choose an option (1/2/3/4/5/6): ").strip()
            
            if choice == '1':
                display_account_info()
            elif choice == '2':
                upload_bulk_data()
            elif choice == '3':
                search_by_phone()
            elif choice == '4':
                manual_entry()
            elif choice == '5':
                remove_data()
            elif choice == '6':
                print(Fore.GREEN + "Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")
                input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

if __name__ == "__main__":
    # Remove any initial example entry from the bulk_input.txt
    if not os.path.exists(bulk_input_file):
        with open(bulk_input_file, 'w') as f:
            pass  # Leave it empty for the user to upload data

    # Start the main program
    main()
