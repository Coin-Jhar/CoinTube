import os
import re

# Precompile regex patterns for performance
YOUTUBE_PATTERNS = [
    re.compile(r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+(\?.*)?$', re.IGNORECASE),
    re.compile(r'(https?://)?(www\.)?youtube\.com/shorts/.+(\?.*)?$', re.IGNORECASE),
    re.compile(r'(https?://)?(music\.)?youtube\.com/.+(\?.*)?$', re.IGNORECASE),
    re.compile(r'(https?://)?(www\.)?youtube\.com/watch\?v=.+(\&.*)?$', re.IGNORECASE),
    re.compile(r'(https?://)?(www\.)?youtube\.com/embed/.+(\?.*)?$', re.IGNORECASE),
    re.compile(r'(https?://)?(www\.)?youtube\.com/playlist\?list=.+$', re.IGNORECASE)  # Playlist pattern
]

def valid_youtube_link(url: str) -> bool:
    """
    Checks if the given URL is a valid YouTube link.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is a valid YouTube link, False otherwise.
    """
    return any(pattern.match(url) for pattern in YOUTUBE_PATTERNS)

def get_user_input(use_template=False):  # Add use_template parameter
    """Gets the YouTube URL, output directory, quality, and format from the user."""
    url = input("Enter the YouTube video/playlist URL: ")

    while not valid_youtube_link(url):
        print("Invalid YouTube URL. Please try again.")
        url = input("Enter the YouTube video/playlist URL: ")

    default_dir = "downloads"
    os.makedirs(default_dir, exist_ok=True)

    output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir

    # Validate output directory path
    while not os.path.isdir(output_dir) or not os.access(output_dir, os.W_OK):
        print("Invalid output directory or no write permissions. Please try again.")
        output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir

    if not use_template:  # Only prompt if not using a template
        valid_qualities = ["best", "high", "medium", "low"]
        quality = input("Enter desired quality (best/high/medium/low, default: best): ") or "best"
