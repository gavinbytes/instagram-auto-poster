import os
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

def find_oldest_file(folder_path):
    """
    Find the oldest file in the specified folder based on creation time (macOS st_birthtime).
    
    Args:
        folder_path (str): Path to the folder to search for files.
        
    Returns:
        str or None: Path to the oldest file, or None if folder is empty or doesn't exist.
    """
    folder = Path(folder_path)
    
    # Check if folder exists
    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return None
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return None
    
    valid_extensions = {'.jpeg', '.jpg', '.mov', '.mp4'}
    oldest_file = None
    oldest_birthtime = float('inf')
    
    # Iterate through all files in the folder
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            try:
                stats = os.stat(file_path)
                creation_timestamp = stats.st_birthtime
                if creation_timestamp < oldest_birthtime:
                    oldest_birthtime = creation_timestamp
                    oldest_file = str(file_path)
            except AttributeError:
                print(f"Warning: Could not retrieve birthtime for {file_path}, skipping.")
                continue
            except OSError as e:
                print(f"Error accessing {file_path}: {e}")
                continue
    
    if oldest_file:
        # Convert the oldest file's creation timestamp to human-readable datetime in CST
        creation_datetime = datetime.fromtimestamp(oldest_birthtime, tz=ZoneInfo("America/Chicago"))
        formatted_datetime = creation_datetime.strftime('%Y-%m-%d %H:%M:%S %Z')
        print(f"Oldest file found: {oldest_file} (Created: {formatted_datetime})")
    else:
        print("No valid files found in the folder.")
    
    return oldest_file

if __name__ == "__main__":
    # Replace with your folder path (relative or absolute)
    folder_path = "./media_folder"  # or "/Users/yourname/project/media_folder"
    oldest_file = find_oldest_file(folder_path)
    print(f"Result: {oldest_file}")