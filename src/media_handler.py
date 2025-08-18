"""
Media handler module for selecting and managing media files.
"""
import os
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image

# Define paths
PHOTODUMP_PATH = "photodump"
POSTED_MEDIA_PATH = "posted_media"

def get_photo_creation_date(local_path):
    """Extract creation date from photo EXIF or fallback to file creation time."""
    try:
        with Image.open(local_path) as img:
            exif_data = img.getexif()
            if exif_data:
                # EXIF tag 36867: DateTimeOriginal
                date_str = exif_data.get(36867)
                if date_str:
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S').replace(tzinfo=ZoneInfo("America/Chicago"))
    except Exception as e:
        logging.warning(f"Failed to extract EXIF date for {local_path}: {e}")
    
    # Fallback to file creation time (st_birthtime for macOS)
    try:
        stats = os.stat(local_path)
        creation_time = stats.st_birthtime
        return datetime.fromtimestamp(creation_time, tz=ZoneInfo("America/Chicago"))
    except AttributeError:
        logging.warning(f"st_birthtime not available for {local_path}, using current time")
        return datetime.now(tz=ZoneInfo("America/Chicago"))
    except Exception as e:
        logging.error(f"Failed to get file creation time for {local_path}: {e}")
        return datetime.now(tz=ZoneInfo("America/Chicago"))

def get_oldest_media():
    """
    Return the path, filename, and creation date of the oldest media file in photodump/.
    
    Returns:
        tuple: (file_path, filename, creation_date) or (None, None, None) if no valid files.
    """
    folder = Path(PHOTODUMP_PATH)
    
    # Check if folder exists
    if not folder.exists():
        logging.error(f"Directory {PHOTODUMP_PATH} does not exist")
        return None, None, None
    if not folder.is_dir():
        logging.error(f"'{PHOTODUMP_PATH}' is not a directory")
        return None, None, None
    
    valid_extensions = {'.jpeg', '.jpg', '.mov', '.mp4', '.png'}
    file_data = []
    
    # Iterate through all files in the folder
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            try:
                filename = file_path.name
                creation_date = get_photo_creation_date(file_path)
                file_data.append((str(file_path), filename, creation_date))
            except Exception as e:
                logging.warning(f"Skipping {file_path} due to error: {e}")
                continue
    
    if not file_data:
        logging.info(f"No valid media files found in {PHOTODUMP_PATH}")
        return None, None, None
    
    # Get the oldest file
    oldest_file = min(file_data, key=lambda x: x[2])
    logging.info(f"Oldest file found: {oldest_file[1]} (Created: {oldest_file[2].strftime('%Y-%m-%d %H:%M:%S %Z')})")
    return oldest_file[0], oldest_file[1], oldest_file[2]

def move_to_posted_folder(filename):
    """Move the file from photodump/ to posted_media/ with timestamp prefix."""
    if not os.path.exists(POSTED_MEDIA_PATH):
        os.makedirs(POSTED_MEDIA_PATH)
    
    src_path = os.path.join(PHOTODUMP_PATH, filename)
    timestamp = datetime.now(tz=ZoneInfo("America/Chicago")).strftime("%Y%m%d_%H%M%S")
    dst_filename = f"{timestamp}_{filename}"
    dst_path = os.path.join(POSTED_MEDIA_PATH, dst_filename)
    
    try:
        os.rename(src_path, dst_path)
        logging.info(f"Moved {filename} to {dst_path}")
    except Exception as e:
        logging.error(f"Failed to move {filename} to {POSTED_MEDIA_PATH}: {e}")