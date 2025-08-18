"""
Main entry point for the Instagram Auto-Poster application.
Posts the 10 oldest photos from local media at once, using EXIF metadata for creation date.
"""
import logging
from datetime import datetime
from .media_handler import get_oldest_media, move_to_posted_folder
from .instagram_client import get_instagram_client, post_media
from .find_oldest_file import find_oldest_file

# Configure logging to console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_poster.log'),
        logging.StreamHandler()
    ]
)

def job():
    """Post the 10 oldest photos to Instagram and move files."""
    logging.info("Starting job execution to post 10 photos")
    try:
        client = get_instagram_client()
        logging.info("Connected to Instagram")
        
        # Get the 10 oldest photos
        posted_count = 0
        while posted_count < 30:
            local_path, filename, timestamp = get_oldest_media()
            if not local_path:
                logging.info("No more photos to post")
                break
            if not local_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                logging.info(f"Skipping non-photo file: {local_path}")
                move_to_posted_folder(filename)  # Move non-photo to avoid infinite loop
                continue
            
            logging.info(f"Selected photo: {local_path}")
            caption = f"~\nFILENAME:{filename}\nDATE CREATED: {timestamp.strftime('%m/%d/%Y')}"
            logging.info(f"Posting photo with caption: {caption}")
            post_media(client, local_path, caption)
            logging.info(f"Posted photo: {local_path}")
            
            logging.info(f"Moving {filename} to posted folder")
            move_to_posted_folder(filename)
            logging.info(f"Moved {filename} to posted folder")
            posted_count += 1
        
        logging.info(f"Completed posting {posted_count} photos")
    except Exception as e:
        logging.error(f"Job failed: {e}", exc_info=True)

def main():
    """Main function to run the job once."""
    logging.info("Starting Instagram Auto-Poster...")
    job()
    # folder_path = "./photodump"  # or "/Users/yourname/project/media_folder"
    # oldest_file = find_oldest_file(folder_path)
    # print(f"Result: {oldest_file}")

if __name__ == "__main__":
    main()