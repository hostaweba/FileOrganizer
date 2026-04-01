import os
import hashlib
import shutil
from datetime import datetime

def calculate_hash(file_path, block_size=65536):
    """Calculate SHA-256 hash for a file."""
    print(f"Calculating hash for: {file_path}")
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(block_size):
            sha256.update(chunk)
    return sha256.hexdigest()

def find_duplicates(directory):
    """Find duplicate files in a directory based on file hash."""
    files_hash = {}
    duplicates = []

    print(f"\nScanning directory: {directory}")
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            if os.path.isfile(file_path):
                # Calculate file hash
                file_hash = calculate_hash(file_path)

                if file_hash in files_hash:
                    # Append to the duplicates list (hash -> list of files)
                    print(f"Duplicate found: {file_path} and {files_hash[file_hash]} have the same content.")
                    duplicates.append((files_hash[file_hash], file_path))
                else:
                    # Save the file with its hash
                    files_hash[file_hash] = file_path
    return duplicates

def move_older_duplicates(duplicates, target_directory):
    """Move older duplicate files to the target directory."""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    print(f"\nMoving older duplicate files to: {target_directory}")
    
    for original_file, duplicate_file in duplicates:
        # Compare file modification times
        original_time = os.path.getmtime(original_file)
        duplicate_time = os.path.getmtime(duplicate_file)

        if original_time > duplicate_time:
            older_file = duplicate_file
        else:
            older_file = original_file

        # Move the older file to the target directory
        new_path = os.path.join(target_directory, os.path.basename(older_file))
        print(f"Moving {older_file} to {new_path}")
        shutil.move(older_file, new_path)

def main(directory):
    # Directory to move duplicates
    duplicate_dir = "_[sys]_duplicate_files"

    print("\nStarting duplicate file scan...")
    
    # Find duplicates
    duplicates = find_duplicates(directory)

    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate file(s). Moving older duplicates...")
        move_older_duplicates(duplicates, duplicate_dir)
        print("\nProcess completed.")
    else:
        print("\nNo duplicate files found.")

if __name__ == "__main__":
    target_directory = input("Enter the directory to scan for duplicate files: ")
    main(target_directory)
