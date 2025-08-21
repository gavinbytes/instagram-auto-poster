"""
poster.py
Core posting loop for the Instagram Auto-Poster.
"""

import logging
import time
from .media_handler import get_oldest_media, move_to_posted_folder
from .instagram_client import get_instagram_client, post_media

def run(count: int, dry_run: bool = False, delay: int = 0) -> None:
    """
    Post the oldest media to Instagram and move them to the posted folder.

    Args:
        count (int): How many media files to post this run.
        dry_run (bool): If True, simulate posting without sending to Instagram.
        delay (int): Seconds to wait between posts.
    """
    logging.info(f"Starting poster run | count={count} dry_run={dry_run} delay={delay}")

    try:
        client = None if dry_run else get_instagram_client()
        if client:
            logging.info("Connected to Instagram")

        posted_count = 0
        while posted_count < count:
            local_path, filename, timestamp = get_oldest_media()

            if not local_path:
                logging.info("No more media to post")
                break

            if not local_path.lower().endswith(('.jpg', '.jpeg', '.png', '.mov', '.mp4')):
                logging.info(f"Skipping unsupported file: {local_path}")
                move_to_posted_folder(filename)
                continue

            caption = f"~\nFILENAME: {filename}\nDATE CREATED: {timestamp.strftime('%m/%d/%Y')}"
            logging.info(f"Prepared caption: {caption}")

            if dry_run:
                logging.info(f"[DRY RUN] Would post {local_path}")
            else:
                post_media(client, local_path, caption)
                logging.info(f"Posted media: {local_path}")

            if dry_run:
                logging.info(f"[DRY RUN] Would move {filename} to posted folder")
            else:
                move_to_posted_folder(filename)
                logging.info(f"Moved {filename} to posted folder")

            posted_count += 1

            if delay > 0 and posted_count < count:
                logging.info(f"Waiting {delay} seconds before next post...")
                time.sleep(delay)

        logging.info(f"Run complete. Total media processed: {posted_count}")

    except Exception as e:
        logging.error(f"Poster run failed: {e}", exc_info=True)