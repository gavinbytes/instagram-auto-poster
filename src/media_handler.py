"""
Media handler module for selecting and managing media files.
"""
import os
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image
import ffmpeg

# Define paths
PHOTODUMP_PATH = "photodump"
POSTED_MEDIA_PATH = "posted_media"

import os
import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

PHOTODUMP_PATH = "photodump"

def get_oldest_media():
    """
    Return the path, filename, and creation date of the oldest media file in photodump/.
    Returns (file_path, filename, creation_date) or (None, None, None) if none found.
    """
    folder = Path(PHOTODUMP_PATH)
    if not folder.is_dir():
        logging.error(f"{PHOTODUMP_PATH} is not a valid directory")
        return None, None, None

    valid_exts = {".jpeg", ".jpg", ".png", ".mov", ".mp4"}
    file_data = []

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in valid_exts:
            try:
                # Try file creation time (st_birthtime), fallback to modified time
                stats = os.stat(file_path)
                creation_time = getattr(stats, "st_birthtime", stats.st_mtime)
                creation_date = datetime.fromtimestamp(creation_time, tz=ZoneInfo("America/Los_Angeles"))
                file_data.append((str(file_path), file_path.name, creation_date))
            except Exception as e:
                logging.warning(f"Skipping {file_path}: {e}")

    if not file_data:
        logging.info(f"No valid media files found in {PHOTODUMP_PATH}")
        return None, None, None

    oldest = min(file_data, key=lambda x: x[2])
    logging.info(f"Oldest file: {oldest[1]} (Created: {oldest[2]})")
    return oldest

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