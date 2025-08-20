"""
Main entry point for the Instagram Auto-Poster application.
Posts the 10 oldest photos from local media at once, using EXIF metadata for creation date.
"""
import argparse
import logging
import sys
from .poster import run

def main():
    """Parse CLI arguments and run the poster."""
    parser = argparse.ArgumentParser(description="Instagram Auto-Poster")
    parser.add_argument('--count', type=int, default=10, help='Number of photos to post')
    parser.add_argument('--dry-run', action='store_true', help='Run without posting to Instagram')
    parser.add_argument('--delay', type=int, default=0, help='Delay in seconds between posts')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("instagram_poster.log"),
            logging.StreamHandler()
        ],
        force=True
    )
    logging.info("Starting Instagram Auto-Poster...")
    try:
        run(args.count, args.dry_run, args.delay)
    except Exception as e:
        logging.error(f"Main execution failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()