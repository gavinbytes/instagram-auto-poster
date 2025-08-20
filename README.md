# Instagram Auto-Poster

## Overview
The Instagram Auto-Poster is a Python-based application designed to automate the posting of media (images and videos) to Instagram. It selects the oldest files from a `photodump/` directory using EXIF metadata, video metadata, or file creation time, processes them for Instagram compatibility, and moves them to a `posted_media/` directory after posting. The project is maintained under the GitHub repository `instagram-auto-poster`.

## Project Structure
```
instagram-auto-poster/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── instagram_client.py
│   ├── main.py
│   ├── media_handler.py
│   └── poster.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/instagram-auto-poster.git
   cd instagram-auto-poster
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Instagram credentials in a `.env` file (see Configuration).

## Configuration
Create a `.env` file in the project root with your Instagram credentials:
```
INSTA_USERNAME=your_username
INSTA_PASSWORD=your_password
```

## Usage
Run the application with:
```bash
python src/main.py --count 10 --dry-run --delay 0
```
- `--count`: Number of media files to post (default: 10).
- `--dry-run`: Simulate posting without uploading.
- `--delay`: Seconds between posts (default: 0).

## Development History
- **Initial Commit**: 2 days ago - Initial setup of the Instagram auto-poster project.
- **Recent Update**: 2 hours ago - General improvements ("works good") by Gavin Aguinaqa.

## Contributors
- Gavin Aguinaqa

## License
MIT License (see `LICENSE` file for details).