# Instagram Auto-Poster

A Python application to automatically post the 10 oldest photos from a local `photodump/` folder to Instagram, using EXIF metadata for creation dates and correcting image orientation.

## Features
- Posts 10 photos (`.jpg`, `.jpeg`, `.png`) at once.
- Uses EXIF `DateTimeOriginal` for sorting and captions (`MM/DD/YYYY` format).
- Corrects photo orientation based on EXIF metadata.
- Moves posted photos to `posted_media/` with a timestamp prefix.
- Logs actions to `instagram_poster.log`.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-auto-poster.git
   cd instagram-auto-poster