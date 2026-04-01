import os
import shutil
import csv
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

def calculate_hash(file_path, block_size=65536):
    """Calculate SHA-256 hash for a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(block_size):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_file_info(file_path):
    """Returns a tuple with file size and its hash."""
    try:
        file_size = os.path.getsize(file_path)
        file_hash = calculate_hash(file_path)
        return (file_path, file_size, file_hash)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def print_progress(current, total, task="Processing", elapsed_time=0):
    """Print progress percentage and estimated time remaining."""
    percent = (current / total) * 100
    avg_time_per_file = elapsed_time / current if current > 0 else 0
    estimated_time_remaining = avg_time_per_file * (total - current)
    minutes, seconds = divmod(estimated_time_remaining, 60)
    
    print(f"\r{task}: {percent:.2f}% complete | "
          f"Elapsed time: {elapsed_time:.2f}s | "
          f"Estimated time remaining: {int(minutes)}m {int(seconds)}s", end='')

def find_duplicates(target_directory, max_workers=4):
    """Find duplicate files in a target_directory using multithreading and file size filtering."""
    files_hash = {}
    duplicates = []

    print(f"Scanning target_directory: {target_directory}")

    # Gather all file paths
    file_paths = []
    for dirpath, _, filenames in os.walk(target_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)

    total_files = len(file_paths)
    print(f"Found {total_files} file(s) to scan.")

    processed_files = 0
    start_time = time.time()

    # Use ThreadPoolExecutor to calculate file hashes in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(get_file_info, file_path): file_path for file_path in file_paths}
        
        for future in as_completed(future_to_file):
            result = future.result()
            processed_files += 1

            # Update progress
            elapsed_time = time.time() - start_time
            print_progress(processed_files, total_files, task="Scanning files", elapsed_time=elapsed_time)

            if result:
                file_path, file_size, file_hash = result

                # Only consider files with the same size and hash as duplicates
                if file_hash in files_hash:
                    print(f"\nDuplicate found: {file_path} (original: {files_hash[file_hash]})")
                    duplicates.append((files_hash[file_hash], file_path))
                else:
                    files_hash[file_hash] = file_path

    print(f"\nFinished scanning. Found {len(duplicates)} duplicate file(s).")
    return duplicates

def move_existing_duplicates_to_archive(duplicate_dir):
    """Move existing files in the duplicate directory to an archive folder based on the current date and time, excluding CSV files."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_dir = os.path.join(duplicate_dir, f"archive_{timestamp}")
    
    if not os.path.exists(duplicate_dir):
        print(f"Duplicate directory {duplicate_dir} does not exist.")
        return  # Nothing to move if the folder doesn't exist

    if os.listdir(duplicate_dir):  # Only move if there are files in the folder
        os.makedirs(archive_dir, exist_ok=True)
        for filename in os.listdir(duplicate_dir):
            file_path = os.path.join(duplicate_dir, filename)
            if os.path.isfile(file_path):
                if filename.endswith('.csv'):
                    print(f"Skipping CSV file: {file_path}")
                    continue  # Skip the CSV files
                
                try:
                    # Attempt to move the file to the archive folder
                    shutil.move(file_path, archive_dir)
                except PermissionError as e:
                    # Skip the file if it's being used by another process
                    print(f"PermissionError: Skipping {file_path}. It is being used by another process.")
                except Exception as e:
                    # Handle other exceptions if necessary
                    print(f"Error: Could not move {file_path}. {e}")
    else:
        print(f"No existing duplicates to move to archive.")

def move_older_duplicates(duplicates, target_directory):
    """Move older duplicate files to the target_directory and save the report."""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"Created directory: {target_directory}")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_file = os.path.join(target_directory, f'duplicate_report_{timestamp}.csv')

    total_duplicates = len(duplicates)
    processed_duplicates = 0
    start_time = time.time()

    # Open CSV report file for writing
    with open(report_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Original File', 'Duplicate File', 'Status'])  # Write header

        for original_file, duplicate_file in duplicates:
            try:
                # Compare file modification times
                original_time = os.path.getmtime(original_file)
                duplicate_time = os.path.getmtime(duplicate_file)

                # Determine the older file
                if original_time > duplicate_time:
                    older_file = duplicate_file
                else:
                    older_file = original_file

                # Write the pair to the CSV file
                writer.writerow([original_file, duplicate_file, 'Moved'])

                # Move the older file to the target directory
                new_path = os.path.join(target_directory, os.path.basename(older_file))
                
                # Ensure no file overwrites another
                if os.path.exists(new_path):
                    base, ext = os.path.splitext(new_path)
                    counter = 1
                    while os.path.exists(f"{base}_{counter}{ext}"):
                        counter += 1
                    new_path = f"{base}_{counter}{ext}"

                shutil.move(older_file, new_path)

            except FileNotFoundError:
                # Log and write the error for files not found
                print(f"File not found: {original_file} or {duplicate_file}. Skipping...")
                writer.writerow([original_file, duplicate_file, 'File not found'])
            except Exception as e:
                # Handle other exceptions if necessary
                print(f"Error: Could not move {older_file}. {e}")
                writer.writerow([original_file, duplicate_file, 'Error moving file'])

            # Update progress
            processed_duplicates += 1
            elapsed_time = time.time() - start_time
            print_progress(processed_duplicates, total_duplicates, task="Moving duplicates", elapsed_time=elapsed_time)

    print(f"\nAll older duplicates moved to {target_directory} and saved to {report_file}.")

def main_menu():
    # Set the source folder to the location where the instructions file was found
    source_folder = "E:\\"
    print(f"Set location to: {source_folder}")

    while True:
        input("\n\n ---------------------[Press any key to continue]")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(61*"=" + "\n    Menu: Organize Files by Date and Extension.\n" + 61*"="+"\n")
        print("1. [Organize files] \n--> Skip folders and files that have '_[sys]_' in their name.\n")
        print("6. [Separate Duplicate files]")
        print("0. [Exit]\n\n" + 61*"=")
        
        choice = input("Enter your choice (1/6/0): ").strip()

        if choice == '1':
            print('You chose option 1')

        elif choice == '6': 
            # Directory to move duplicates
            duplicate_dir = os.path.join(source_folder, "_[sys]_duplicate_files")
    
            # Find duplicates
            print(f"Don't type anything and hit enter to scan {source_folder}")
            target_choice = input(f"Type which directory you want to scan from {source_folder}\n -->")
            if target_choice == "":
                target_directory = source_folder
            else:
                target_directory = os.path.join(source_folder, target_choice)
            
            duplicates = find_duplicates(target_directory)
            
            # Move existing duplicates to archive before processing new ones
            move_existing_duplicates_to_archive(duplicate_dir)

            if duplicates:
                print(f"Found {len(duplicates)} duplicate file(s). Moving older duplicates...")
                move_older_duplicates(duplicates, duplicate_dir)
                print("Process completed.")
            else:
                print("No duplicate files found.")
                
        elif choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5 or 0.")

if __name__ == "__main__":
    main_menu()
