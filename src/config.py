"""
Configuration module for loading environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Instagram credentials
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")

# Validate required environment variables
if not all([INSTA_USERNAME, INSTA_PASSWORD]):
    raise ValueError("Missing required environment variables. Check .env file.")