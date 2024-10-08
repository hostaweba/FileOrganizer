# version1.0.0
'''
1). The program will recursively search all drives (D: to Z:) for the instructions.csv and _[sys]_instructions.csv file.
2). If the file is found, it will check if the second line contains "set location".
3). If the condition is met, it will use the directory where the file is found as the source_folder.
4). If the file is not found or does not contain "set location", an error will be printed, and the program will exit.
'''
# version1.0.1_updates
'''
1). Check for _[sys]_ in the full file path:
    *). The script now checks the full path (file_path) for the presence of _[sys]_. If any part of the file path contains _[sys]_, the file is skipped.
    *). This ensures that files inside any folder (or subfolder) starting with _[sys]_ are not moved or processed.

2). Skipping directories that have _[sys]_ in the path:
    *). Similarly, folders with _[sys]_ anywhere in their path are skipped.
    
Note: It will ignore the directory and file if any part of the name contains "_[sys]_". For example, "random_[sys]_name".

'''
#------version1.0.2_updates
'''
new function --> organize_files_ignores_All(source_folder)

1). Scans only directories with '_[scan]_' in their name.
2). Organizes files by date and extension, and ignores others. 

new functions --> organize_files_scan_only_listed_dirs(source_folder, directories_to_scan)
                  read_directories_from_csv(file_path)

1). Reads directories from a CSV file and organizes files only within listed directories, ignoring others.
note: it will automatically find csv file for instructions.

2). add option to go back in "Available csv files" menu
'''

import os
import shutil
import csv
from datetime import datetime
from time import sleep

# Function to organize files by date and extension (looks into subfolders)
def organize_files_by_date_and_extension(source_folder):
    csv_data = []
    old_structure_folder = os.path.join(source_folder, '_[sys]_old_structure')

    # Create _[sys]_old_structure folder if it doesn't exist
    if not os.path.exists(old_structure_folder):
        os.makedirs(old_structure_folder)

    # Traverse all files and subfolders inside source_folder
    for foldername, subfolders, filenames in os.walk(source_folder):
        # Skip folders and files if their path contains any part that starts with _[sys]_
        if '_[sys]_' in foldername:
            print(f"Skipping folder and its contents: {foldername}")
            continue  # Ignore this folder and everything inside it

        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Skip files if any part of their path contains _[sys]_
            if '_[sys]_' in file_path:
                print(f"Skipping file: {file_path} as it's part of _[sys]_")
                continue

            # Get the file's modification time
            modification_time = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(modification_time)
            year = date.strftime('%Y')
            month = date.strftime('%m')

            # Create year and month folders in the source directory
            year_folder = os.path.join(source_folder, year)
            month_folder = os.path.join(year_folder, month)

            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            if not os.path.exists(month_folder):
                os.makedirs(month_folder)

            # Create extension folder
            extension = filename.split('.')[-1]
            extension_folder = os.path.join(month_folder, extension)

            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)

            # Move the file to the appropriate folder
            new_file_path = os.path.join(extension_folder, filename)
            shutil.move(file_path, new_file_path)
            print(f"Moved file {file_path} to {new_file_path}")

            # Collect data for CSV
            csv_data.append({
                'file_path': file_path,
                'new_path': new_file_path,
                'modification_time': date.strftime('%Y-%m-%d %H:%M:%S')
            })

    # Save CSV data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'_[sys]_old_structure_{timestamp}.csv'
    csv_filepath = os.path.join(old_structure_folder, csv_filename)

    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['file_path', 'new_path', 'modification_time'])
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"CSV file saved as {csv_filepath}")


#------version1.0.2
def organize_files_ignores_All(source_folder):
    """
    Scans only directories with '_[scan]_' in their name.
    Organizes files by date and extension, and ignores others.
    """
    
    csv_data = []
    old_structure_folder = os.path.join(source_folder, '_[sys]_old_structure')

    if not os.path.exists(old_structure_folder):
        os.makedirs(old_structure_folder)

    for foldername, subfolders, filenames in os.walk(source_folder):
        # Check if the current foldername contains '_[scan]_' in its name
        if '_[scan]_' not in os.path.basename(foldername):
            print(f"Skipping folder and its contents: {foldername}")
            continue

        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Get the file's modification time
            modification_time = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(modification_time)
            year = date.strftime('%Y')
            month = date.strftime('%m')

            # Create year and month folders in the source directory
            year_folder = os.path.join(source_folder, year)
            month_folder = os.path.join(year_folder, month)

            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            if not os.path.exists(month_folder):
                os.makedirs(month_folder)

            # Create extension folder
            extension = filename.split('.')[-1]
            extension_folder = os.path.join(month_folder, extension)

            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)

            # Move the file to the appropriate folder
            new_file_path = os.path.join(extension_folder, filename)
            shutil.move(file_path, new_file_path)
            print(f"Moved file {file_path} to {new_file_path}")

            # Collect data for CSV
            csv_data.append({
                'file_path': file_path,
                'new_path': new_file_path,
                'modification_time': date.strftime('%Y-%m-%d %H:%M:%S')
            })

    # Save CSV data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'_[sys]_old_structure_{timestamp}.csv'
    csv_filepath = os.path.join(old_structure_folder, csv_filename)

    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['file_path', 'new_path', 'modification_time'])
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"CSV file saved as {csv_filepath}")


def read_directories_from_csv(file_path):
    directories = []
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                if row and len(row) > 1 and row[1].strip():  # Ensure there is a directory path
                    directories.append(row[1].strip())
    except Exception as e:
        print(f"Error reading CSV file: {e}")
    return directories


def organize_files_scan_only_listed_dirs(source_folder, directories_to_scan):
    csv_data=[]
    old_structure_folder = os.path.join(source_folder, '_[sys]_old_structure')
    
    if not os.path.exists(old_structure_folder):
        os.makedirs(old_structure_folder)    
    
    # Get absolute paths for directories to scan
    absolute_dirs_to_scan = [os.path.join(source_folder, d) for d in directories_to_scan]

    for foldername, subfolders, filenames in os.walk(source_folder):
        # Check if current folder is in the list of directories to scan
        if foldername not in absolute_dirs_to_scan:
            print(f"Skipping folder and its contents: {foldername}")
            continue

        for filename in filenames:
            file_path = os.path.join(foldername, filename)

            # Skip files if any part of their path contains _[sys]_
            if '_[sys]_' in file_path:
                print(f"Skipping file: {file_path} as it's part of _[sys]_")
                continue

            # Get the file's modification time
            modification_time = os.path.getmtime(file_path)
            date = datetime.fromtimestamp(modification_time)
            year = date.strftime('%Y')
            month = date.strftime('%m')

            # Create year and month folders in the source directory
            year_folder = os.path.join(source_folder, year)
            month_folder = os.path.join(year_folder, month)

            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

            if not os.path.exists(month_folder):
                os.makedirs(month_folder)

            # Create extension folder
            extension = filename.split('.')[-1]
            extension_folder = os.path.join(month_folder, extension)

            if not os.path.exists(extension_folder):
                os.makedirs(extension_folder)

            # Move the file to the appropriate folder
            new_file_path = os.path.join(extension_folder, filename)
            shutil.move(file_path, new_file_path)
            print(f"Moved file {file_path} to {new_file_path}")

            # Collect data for CSV
            csv_data.append({
                'file_path': file_path,
                'new_path': new_file_path,
                'modification_time': date.strftime('%Y-%m-%d %H:%M:%S')
            })

    # Save CSV data
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f'_[sys]_old_structure_{timestamp}.csv'
    csv_filepath = os.path.join(old_structure_folder, csv_filename)

    with open(csv_filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['file_path', 'new_path', 'modification_time'])
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"CSV file saved as {csv_filepath}")

# ---version1.0.2_update finish


# Function to revert files back to their original paths based on CSV
def revert_files_from_csv(source_folder, csv_file):
    old_structure_folder = os.path.join(source_folder, '_[sys]_old_structure')

    if not os.path.exists(old_structure_folder):
        print("Error: _[sys]_old_structure folder does not exist.")
        return

    csv_filepath = os.path.join(old_structure_folder, csv_file)

    if not os.path.exists(csv_filepath):
        print(f"Error: CSV file {csv_filepath} does not exist.")
        return

    with open(csv_filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            old_path = row['file_path']
            new_path = row['new_path']

            if os.path.exists(new_path):
                shutil.move(new_path, old_path)
                print(f"Reverted {new_path} to {old_path}")

    # Remove empty directories
    remove_empty_directories(source_folder)

# Function to remove empty directories
def remove_empty_directories(folder):
    for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
        # Skip directories if their path contains any part that starts with _[sys]_
        if '_[sys]_' in dirpath:
            continue
        if not os.listdir(dirpath):  # Check if directory is empty
            print(f"Removing empty directory {dirpath}")
            os.rmdir(dirpath)

# Function to list CSV files in a folder
def list_csv_files(folder):
    return [f for f in os.listdir(folder) if f.endswith('.csv')]

# Function to search for the instructions file across all drives
def find_instructions_file():
    drives = [f"{chr(drive)}:\\" for drive in range(ord('D'), ord('Z')+1) if os.path.exists(f"{chr(drive)}:\\")]

    for drive in drives:
        for root, dirs, files in os.walk(drive):
            for file in files:
                if file.lower() == 'instructions.csv' or file.lower() == '_[sys]_instructions.csv':
                    instructions_path = os.path.join(root, file)
                    print(f"Found instructions file at: {instructions_path}")
                    return instructions_path
    return None

# Function to validate the instructions file
def validate_instructions_file(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2 and 'set location' in lines[1].strip().lower():
                return True
            else:
                print(f"Error: The second line does not contain 'set location'.")
                return False
    except Exception as e:
        print(f"Error reading instructions file: {e}")
        return False

# Main menu function
def main_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Find the instructions file
    instructions_file = find_instructions_file()

    if instructions_file is None:
        print("Error: No 'instructions.csv' or '_[sys]_instructions.csv' file found.")
        input("Press any key to exit...")
        return

    # Validate the instructions file
    if not validate_instructions_file(instructions_file):
        input("Press any key to exit...")
        return

    # Set the source folder to the location where the instructions file was found
    source_folder = os.path.dirname(instructions_file)
    print(f"Set location to: {source_folder}")

    # Read the directories to scan from the instructions file
    directories_to_scan = read_directories_from_csv(instructions_file)
    
    while True:
        input("\n\n ---------------------[Press any key to continue]")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(61*"=" + "\n    Menu: Organize Files by Date and Extension.\n" + 61*"="+"\n")
        print("1. [Organize files] \n--> Skip folders and files that have '_[sys]_' in their name.\n")
        print("2. [Organize files] \n--> Only scan folders that have '_[scan]_' in their name.\n")
        print("3. [Organize files] \n--> Only scan that mention in '_[sys]_instructions.csv' file.\n")        
        print(61*"-" + "\n\n4. [Revert files from CSV]")
        print("5. [Open directory to see history]")
        print("0. [Exit]\n\n" + 61*"=")
        
        choice = input("Enter your choice (1/2/3/4/5/0): ").strip()

        if choice == '1':
            organize_files_by_date_and_extension(source_folder)
        elif choice == '2':
            organize_files_ignores_All(source_folder)
        elif choice == '3':    
            organize_files_scan_only_listed_dirs(source_folder, directories_to_scan)
        elif choice == '4':
            old_structure_folder = os.path.join(source_folder, '_[sys]_old_structure')
            if os.path.exists(old_structure_folder):
                csv_files = list_csv_files(old_structure_folder)
                if csv_files:
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("Available CSV files:")
                        for i, file in enumerate(csv_files):
                            print(f"{i + 1}. {file}")
                        print("0. Go Back")
                        try:
                            csv_choice = input("Select a CSV file by number: ").strip()
                            if csv_choice == '0':
                                break  # Exit the inner loop and return to the main menu
                            csv_choice = int(csv_choice)
                            if 1 <= csv_choice <= len(csv_files):
                                csv_filename = csv_files[csv_choice - 1]
                                revert_files_from_csv(source_folder, csv_filename)
                            else:
                                print("Invalid choice. Please select a number from the list.")
                        except ValueError:
                            print("Invalid input. Please enter a valid number.")
                else:
                    print("No CSV files found in _[sys]_old_structure.")
            else:
                print("Error: _[sys]_old_structure folder does not exist.")         
        elif choice == '5':
            directory = os.path.join(source_folder, "_[sys]_old_structure")
            if os.path.exists(directory):
                os.startfile(directory)
            else:
                print("Error: _[sys]_old_structure folder does not exist.")
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5 or 0.")

if __name__ == "__main__":
    main_menu()
