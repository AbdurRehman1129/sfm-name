import json
import os
import platform
import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the file paths
bulk_input_file = 'bulk_input.txt'  # File for uploading data
safeum_file = 'safeum.json'  # File to store data

# Function to clear the terminal screen
def clear_screen():
    system_name = platform.system().lower()
    os.system('cls' if system_name == 'windows' else 'clear')

# Function to display the banner
def display_banner():
    banner = pyfiglet.Figlet(font="small")
    banner_text = banner.renderText("DARK DEVIL")
    
    # Center the banner text
    terminal_width = os.get_terminal_size().columns
    centered_banner = '\n'.join(line.center(terminal_width) for line in banner_text.splitlines())
    print(Fore.CYAN + centered_banner)
    
    # Center the author line
    author_line = f"Author/Github: {Fore.GREEN}@AbdurRehman1129"
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

# Function to display stored account info with numbering
def display_account_info():
    data = load_data()
    if not data:
        print(Fore.RED + "No account info stored.")
    else:
        print(Fore.CYAN + "Stored Accounts:")
        for i, (username, phone) in enumerate(data.items(), start=1):
            print(f"{Fore.YELLOW}{i}. {Fore.GREEN}Account: {Style.RESET_ALL}{username} {Fore.YELLOW}Phone: {Style.RESET_ALL}{phone}")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to display only phone numbers
def display_phone_numbers():
    data = load_data()
    if not data:
        print(Fore.RED + "No phone numbers stored.")
    else:
        print(Fore.CYAN + "Phone Numbers:")
        for i, phone in enumerate(data.values(), start=1):
            print(f"{Fore.YELLOW}{i}. {Fore.GREEN}{phone}")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Function to upload bulk data from the bulk_input.txt file
def upload_bulk_data():
    if not os.path.exists(bulk_input_file):
        print(Fore.RED + f"{bulk_input_file} not found, please create this file with the data.")
        input(Fore.WHITE + "\nPress Enter to return to the menu...")
        return

    data = load_data()
    with open(bulk_input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '@' in line:
                username, phone = line.split('@', 1)
                data[username] = phone.replace(" ", "")
            else:
                print(Fore.RED + f"Skipping invalid line: {line}")
    save_data(data)
    print(Fore.GREEN + f"Bulk data from {bulk_input_file} has been uploaded successfully!")
    input(Fore.WHITE + "\nPress Enter to return to the menu...")

# Function to search by phone number or username
def search_by_phone():
    data = load_data()
    while True:
        search_input = input(Fore.YELLOW + "Enter Phone Number or Username to search: ").strip()
        found = False
        if search_input in data:
            print(f"{Fore.GREEN}Username {search_input} is associated with phone number: {Style.RESET_ALL}{data[search_input]}")
            found = True
        else:
            for username, phone in data.items():
                if phone == search_input:
                    print(f"{Fore.GREEN}Phone number {search_input} is associated with username: {Style.RESET_ALL}{username}")
                    found = True
                    break
        if not found:
            print(Fore.RED + f"No account found for {search_input}")
        if input(Fore.YELLOW + "Do you want to search again? (Y/N): ").strip().lower() != 'y':
            break

# Function to remove account data (by username or phone number)
def remove_data():
    data = load_data()
    while True:
        remove_input = input(Fore.YELLOW + "Enter Username or Phone Number to remove: ").strip()
        if remove_input in data:
            del data[remove_input]
            save_data(data)
            print(Fore.GREEN + f"Account with username {remove_input} has been removed.")
        else:
            found = False
            for username, phone in data.items():
                if phone == remove_input:
                    del data[username]
                    save_data(data)
                    print(Fore.GREEN + f"Account with phone number {remove_input} has been removed.")
                    found = True
                    break
            if not found:
                print(Fore.RED + "No account found with the provided username/phone number.")
        if input(Fore.YELLOW + "Do you want to remove another account? (Y/N): ").strip().lower() != 'y':
            break

# Function for manual entry
def manual_entry():
    data = load_data()
    
    while True:
        username = input(
            Fore.YELLOW + "Enter " +
            Fore.CYAN + "Username" +
            Fore.YELLOW + " (or type " +
            Fore.RED + "'NO'" +
            Fore.YELLOW + " to stop): "
        ).strip()
        
        # Check if the user wants to stop
        if username.lower() == 'no':
            print(Fore.GREEN + "Exiting manual entry...")
            break
        
        # Ensure username is unique
        if username in data:
            print(Fore.RED + f"Username '{username}' already exists. Please enter a different username.")
            continue
        
        while True:
            try:
                # Ask for phone number and validate input
                phone = input(
                    Fore.YELLOW + f"Enter " +
                    Fore.CYAN + "Phone Number" +
                    Fore.YELLOW + f" for {Fore.CYAN}'{username}': "
                ).strip()
                
                # Ensure phone is a number and unique
                if not phone.isdigit():
                    print(Fore.RED + "Phone number must be numeric. Please try again.")
                    continue
                if phone in data.values():
                    print(Fore.RED + f"Phone number '{phone}' already exists. Please enter a different number.")
                    continue
                
                # Save valid username and phone
                data[username] = phone
                save_data(data)
                print(Fore.GREEN + f"Account for {Fore.CYAN}'{username}' {Fore.GREEN}and phone {Fore.CYAN}'{phone}' {Fore.GREEN}added successfully!")
                break  # Exit the phone number input loop
            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}. Please try again.")


def format_numbers_for_email():
    """
    Formats and displays all phone numbers in a single comma-separated line,
    suitable for email sending.
    """
    data = load_data()
    if not data:
        print(Fore.RED + "No data available to format.")
    else:
        # Extract phone numbers and join them with commas
        phone_numbers = ', '.join(data.values())
        print(Fore.GREEN + "Phone numbers in email-sending format:\n")
        print(Fore.YELLOW + phone_numbers)
    input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue

# Main function to display menu
def main():
    while True:
        clear_screen()  # Clear screen at the beginning of each run
        display_banner()  # Display the banner
        print(Fore.YELLOW + "1." + Fore.GREEN + " Display Accounts")
        print(Fore.YELLOW + "2." + Fore.GREEN + " Upload Bulk Accounts")
        print(Fore.YELLOW + "3." + Fore.GREEN + " Search by Phone Number or Username")
        print(Fore.YELLOW + "4." + Fore.GREEN + " Manually Enter Account")
        print(Fore.YELLOW + "5." + Fore.GREEN + " Remove Account")
        print(Fore.YELLOW + "6." + Fore.GREEN + " Display All Phone Numbers in Email-Sending Format")
        print(Fore.YELLOW + "7." + Fore.GREEN + " Exit")
        
        try:
            choice = input(Fore.WHITE + "Choose an option (1/2/3/4/5/6/7): ").strip()
            
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
                format_numbers_for_email()
            elif choice == '7':
                print(Fore.GREEN + "Goodbye!")
                break
            else:
                print(Fore.RED + "Invalid choice, please try again.")
                input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}")
            input(Fore.WHITE + "\nPress Enter to return to the menu...")  # Wait for user to continue


if __name__ == "__main__":
    if not os.path.exists(bulk_input_file):
        open(bulk_input_file, 'w').close()
    main()
