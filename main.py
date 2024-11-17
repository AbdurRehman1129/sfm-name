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

# Function to manually enter username and phone number
def manual_entry():
    username = input(Fore.YELLOW + "Enter Username: ").strip()
    phone = input(Fore.YELLOW + "Enter Phone Number (with no spaces): ").strip().replace(" ", "")
    
    # Validate phone number (make sure it's numeric)
    if not phone.isdigit():
        print(Fore.RED + "Invalid phone number. Please enter a valid number.")
        input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue
        return
    
    data = load_data()
    data[username] = phone
    save_data(data)
    print(Fore.GREEN + "Account info added successfully!")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Main function to display menu
def main():
    while True:
        clear_screen()  # Clear screen at the beginning of each run
        display_banner()  # Display the banner
        print(Fore.MAGENTA + "Safeum Account Info")
        print(Fore.MAGENTA + "1. Display Account Info")
        print(Fore.MAGENTA + "2. Upload Bulk Account Info (from bulk_input.txt)")
        print(Fore.MAGENTA + "3. Search by Phone Number")
        print(Fore.MAGENTA + "4. Manually Enter Account Info")
        print(Fore.MAGENTA + "5. Exit")
        
        try:
            choice = input(Fore.WHITE + "Choose an option (1/2/3/4/5): ").strip()
            
            if choice == '1':
                display_account_info()
            elif choice == '2':
                upload_bulk_data()
            elif choice == '3':
                search_by_phone()
            elif choice == '4':
                manual_entry()
            elif choice == '5':
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
