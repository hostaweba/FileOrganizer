### Documentation: File Organizer Script

---

### Purpose:
This Python script organizes files in a folder (and its subfolders) based on their modification date and file extension. Additionally, it can revert these changes using a CSV log file. It also supports ignoring any folders or files that start with `_[sys]_`, ensuring no changes are made to them.

### Features:
1. **Organize Files**: Sorts files into folders by year, month, and file extension.
2. **Revert Changes**: Moves files back to their original locations based on a previously saved CSV log.
3. **Ignore System Folders**: Automatically skips any folder or file starting with `_[sys]_`, ensuring system-related files or folders are not affected.
4. **Generate CSV Logs**: Creates a CSV file to log all moves made during organization.
5. **Supports Multiple Drives**: The script searches across all drives from D: to Z: to find the `instructions.csv` or `_sys_instructions.csv` file.

---

### Prerequisites:
1. **Python 3.x** must be installed on your system.
2. Install the necessary Python libraries:
   - **shutil**: For moving files.
   - **csv**: For logging the moved files.
   - **os**: For file system operations.
   - **datetime**: For handling date and time.


