"""
Instagram client module for posting media.
"""
import instagrapi
import logging
import os
import tempfile
import ffmpeg
from PIL import Image
from .config import INSTA_USERNAME, INSTA_PASSWORD

def get_instagram_client():
    """Initialize and return an Instagram client."""
    client = instagrapi.Client()
    try:
        client.login(INSTA_USERNAME, INSTA_PASSWORD)
        return client
    except Exception as e:
        raise ConnectionError(f"Instagram login failed: {e}")

def correct_image_orientation(local_path):
    """Correct image orientation based on EXIF metadata and save to a temporary file."""
    try:
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"oriented_{os.path.basename(local_path)}")
        
        with Image.open(local_path) as img:
            # Apply EXIF orientation
            exif = img.getexif()
            orientation = exif.get(274, 1)  # EXIF tag 274: Orientation
            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
            img.save(temp_file, quality=95)
        
        logging.info(f"Corrected orientation for {local_path}, saved to {temp_file}")
        return temp_file
    except Exception as e:
        logging.warning(f"Failed to correct orientation for {local_path}: {e}")
        return local_path  # Return original path if correction fails

def convert_mp4_to_compatible(local_path):
    """Convert .mp4 or .mov to Instagram-compatible format (H.264, AAC, 1080x1920, 30fps, max 60s)."""
    try:
        # Log original video properties
        probe = ffmpeg.probe(local_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        duration = float(probe['format']['duration'])
        resolution = [int(video_stream['width']), int(video_stream['height'])] if video_stream else [0, 0]
        fps = eval(video_stream['r_frame_rate']) if video_stream else 0
        video_codec = video_stream['codec_name'] if video_stream else 'unknown'
        audio_codec = audio_stream['codec_name'] if audio_stream else 'unknown'
        bitrate = probe['format']['bit_rate'] if 'bit_rate' in probe['format'] else 'unknown'
        aspect_ratio = video_stream['display_aspect_ratio'] if video_stream and 'display_aspect_ratio' in video_stream else 'unknown'
        logging.info(f"Original video properties: duration={duration}s, resolution={resolution}, fps={fps}, "
                     f"video_codec={video_codec}, audio_codec={audio_codec}, bitrate={bitrate}, aspect_ratio={aspect_ratio}")
        
        # Create temporary file for converted video
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"converted_{os.path.basename(local_path)}")
        
        # Convert video using ffmpeg
        stream = ffmpeg.input(local_path, t=60)  # Trim to 60s
        stream = ffmpeg.output(
            stream,
            temp_file,
            vcodec='libx264',  # H.264 video
            acodec='aac',      # AAC audio
            vf='scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
            r=30,              # 30fps
            format='mp4',
            movflags='faststart'
        )
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        # Log converted video properties
        probe = ffmpeg.probe(temp_file)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        duration = float(probe['format']['duration'])
        resolution = [int(video_stream['width']), int(video_stream['height'])] if video_stream else [0, 0]
        fps = eval(video_stream['r_frame_rate']) if video_stream else 0
        video_codec = video_stream['codec_name'] if video_stream else 'unknown'
        audio_codec = audio_stream['codec_name'] if audio_stream else 'unknown'
        bitrate = probe['format']['bit_rate'] if 'bit_rate' in probe['format'] else 'unknown'
        aspect_ratio = video_stream['display_aspect_ratio'] if video_stream and 'display_aspect_ratio' in video_stream else 'unknown'
        logging.info(f"Converted video properties: duration={duration}s, resolution={resolution}, fps={fps}, "
                     f"video_codec={video_codec}, audio_codec={audio_codec}, bitrate={bitrate}, aspect_ratio={aspect_ratio}")
        
        return temp_file
    except Exception as e:
        logging.error(f"Failed to convert video {local_path}: {e}", exc_info=True)
        raise RuntimeError(f"Failed to convert video: {e}")

def post_media(client, local_temp_path, caption):
    """Post media (image or video) to Instagram with provided caption."""
    temp_file = None
    try:
        logging.info(f"Preparing to upload: {local_temp_path}")
        if local_temp_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Correct orientation for images
            temp_file = correct_image_orientation(local_temp_path)
            # Log image properties
            try:
                probe = ffmpeg.probe(temp_file)
                image_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
                resolution = [int(image_stream['width']), int(image_stream['height'])] if image_stream else [0, 0]
                bitrate = probe['format']['bit_rate'] if 'bit_rate' in probe['format'] else 'unknown'
                logging.info(f"Image properties: resolution={resolution}, bitrate={bitrate}")
            except Exception as e:
                logging.warning(f"Failed to log image properties: {e}")
            client.photo_upload(temp_file, caption)
        elif local_temp_path.lower().endswith(('.mp4', '.mov')):
            # Convert .mp4 or .mov to compatible format
            temp_file = convert_mp4_to_compatible(local_temp_path)
            client.video_upload(temp_file, caption)
        else:
            raise ValueError(f"Unsupported media format: {local_temp_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to post media: {e}")
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file):
            try:
                os.remove(temp_file)
                logging.info(f"Removed temporary file: {temp_file}")
            except Exception as e:
                logging.warning(f"Failed to remove temporary file {temp_file}: {e}")