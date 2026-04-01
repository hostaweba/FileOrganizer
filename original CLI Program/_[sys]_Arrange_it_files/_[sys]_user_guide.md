
### How to Use:

#### Step 1: Prepare Instructions File

1. **Instructions File Name**: 
   - Create a file named either `instructions.csv` or `_sys_instructions.csv`.
2. **File Location**: 
   - Place this file on any drive (D: to Z:) where you want the script to look for it.
3. **File Content**: 
   - The second line of this CSV file should contain the phrase `set location`. The script will use the directory containing this file as the base folder for file organization and reversion.

Example:
```
Column1,Column2
set location
```

---

#### Step 2: Running the Script

1. **Launch the Script**:
   - Open a terminal or command prompt.
   - Run the Python script: 
     ```bash
     python organize_files.py
     ```

2. **Automatic Folder Detection**:
   - The script will search for the `instructions.csv` or `_sys_instructions.csv` file across all drives (D: to Z:).
   - Once found, it sets the folder containing this file as the **source folder** for operations.

---

#### Step 3: Menu Options

Once the script finds the instructions file, it will display the following menu:

```text
Menu:
1. Organize files by date and extension
2. Revert files from CSV
3. Exit
```

1. **Option 1: Organize Files**:
   - Select `1` to organize files based on their modification date and extension.
   - Files will be moved to folders based on their year, month, and file type.

2. **Option 2: Revert Files from CSV**:
   - Select `2` to revert the files back to their original locations.
   - The script will ask you to choose a CSV file created during the organization process to guide the reversion.

3. **Option 3: Exit**:
   - Select `3` to exit the script.

---

### File Organization Process:

- **Folder Structure**:
  Files are moved into the following folder structure:
  
  ```
  <Year>/<Month>/<Extension>/<Filename>
  ```

  For example, a file `report.docx` modified in May 2021 will be moved to:
  
  ```
  2021/05/docx/report.docx
  ```

- **CSV Logging**:
  The script generates a CSV file in a folder named `_[sys]_old_structure` inside the source folder. This log contains the old file path, new file path, and modification time.

---

### Reverting Files:

- To revert the files to their original paths:
  1. Select Option `2` from the menu.
  2. The script will display all CSV log files in the `_[sys]_old_structure` folder.
  3. Choose the CSV file corresponding to the organization session you want to revert.
  4. The script will use this CSV log to move all files back to their original locations.

---

### Ignoring Folders and Files:

- The script **automatically ignores** any folder or file whose path contains the string `_[sys]_`. No files in or under such folders will be moved or affected.

Example:
```
_[sys]_folder\
    subfolder\
        file.txt
```
In this case, **`file.txt`** will not be processed because its parent folder starts with `_[sys]_`.

---

### Example Scenario:

1. **Folder Structure Before Organization**:
   ```
   source_folder/
      document.docx
      photo.jpg
      _[sys]_config/
         important.txt
      music.mp3
   ```

2. **Action**:
   After selecting option `1` to organize files, the script will:
   - Move `document.docx` and `photo.jpg` to folders based on their date and extension.
   - **Ignore** the folder `_sys_config` and its contents (`important.txt`).
   - Move `music.mp3` as per its modification date.

3. **Folder Structure After Organization**:
   ```
   source_folder/
      2023/
         09/
            docx/
               document.docx
            jpg/
               photo.jpg
            mp3/
               music.mp3
      _[sys]_old_structure/
         _[sys]_old_structure_20230901_150000.csv
      _[sys]_config/
         important.txt
   ```

---

### Error Handling:

1. **Instructions File Not Found**:
   - If the script cannot find the `instructions.csv` file, it will display the message:
     ```text
     Error: No 'instructions.csv' or '_sys_instructions.csv' file found.
     ```
   - It will then wait for the user to press any key before exiting.

2. **Invalid Instructions File**:
   - If the second line of the instructions file doesn't contain `set location`, the script will display:
     ```text
     Error: The second line does not contain 'set location'.
     ```

---

### Troubleshooting:

- Ensure that `instructions.csv` is correctly named and placed in one of the drives.
- Make sure the folder name or file path doesn't accidentally include `_[sys]_` unless you want it to be ignored.
- Check the CSV logs inside `_[sys]_old_structure` for details on moved files.

---

### Conclusion:

This script provides a flexible and powerful way to organize files in a folder based on modification dates while ensuring that any folders or files starting with `_[sys]_` are ignored. It can also revert these changes using the generated CSV log, making it ideal for managing and maintaining file structures.