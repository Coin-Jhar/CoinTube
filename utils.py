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

def get_user_input(use_template=False, retry_limit=3) -> tuple:
    """
    Prompts the user for YouTube video/playlist URL, output directory, quality, and format.
    
    Args:
        use_template (bool): If True, defaults will be used instead of asking the user for input.
        retry_limit (int): The maximum number of retries for invalid inputs.
    
    Returns:
        tuple: Contains URL, output directory, quality, format, playlist status, subtitle flag, and playlist options.
    """
    url = input("Enter the YouTube video/playlist URL: ")
    
    retry_count = 0
    while not valid_youtube_link(url) and retry_count < retry_limit:
        print("Invalid YouTube URL. Please try again.")
        retry_count += 1
        if retry_count >= retry_limit:
            print("Maximum retry limit reached. Exiting.")
            return None
        url = input("Enter the YouTube video/playlist URL: ")

    default_dir = "downloads"
    os.makedirs(default_dir, exist_ok=True)

    output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir

    # Validate output directory path
    retry_count = 0
    while not os.path.isdir(output_dir) or not os.access(output_dir, os.W_OK):
        print("Invalid output directory or no write permissions. Please try again.")
        retry_count += 1
        if retry_count >= retry_limit:
            print("Maximum retry limit reached. Exiting.")
            return None
        output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir

    if not use_template:  # Only prompt if not using a template
        quality = get_quality_input()
        format = get_format_input()
        download_subs = get_download_subs_input()
    else:
        quality = "best"  
        format = "mp4"
        download_subs = False

    is_playlist = "playlist?list=" in url  # Basic playlist detection
    playlist_options = {}
    if is_playlist:
        playlist_options = get_playlist_options()

    return url, output_dir, quality, format, is_playlist, download_subs, playlist_options

def get_quality_input() -> str:
    """Prompts the user to enter the desired video quality."""
    valid_qualities = ["best", "high", "medium", "low"]
    quality = input("Enter desired quality (best/high/medium/low, default: best): ") or "best"
    while quality not in valid_qualities:
        print(f"Invalid quality. Please choose from {valid_qualities}.")
        quality = input("Enter desired quality: ")
    return quality

def get_format_input() -> str:
    """Prompts the user to enter the desired video format."""
    valid_formats = ["mp4", "webm", "mp3"]
    format = input("Enter desired format (mp4/webm/mp3, default: mp4): ") or "mp4"
    while format not in valid_formats:
        print(f"Invalid format. Please choose from {valid_formats}.")
        format = input("Enter desired format: ")
    return format

def get_download_subs_input() -> bool:
    """Prompts the user to select whether they want to download subtitles."""
    download_subs = input("Download subtitles? (yes/no, default: no): ").lower() or "no"
    return download_subs == "yes"

def get_playlist_options() -> dict:
    """Prompts the user to select specific videos in a playlist."""
    playlist_options = {}
    playlist_selection = input("Select specific videos? (yes/no, default: no): ").lower() or "no"
    if playlist_selection == "yes":
        while True:
            try:
                playlist_options['playlist_items'] = input("Enter comma-separated video indices or ranges (e.g., 1,3,5-7): ")
                break  # Exit loop if input is valid
            except ValueError:
                print("Invalid input. Please enter comma-separated numbers or ranges.")
    return playlist_options
