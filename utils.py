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
    """Checks if the given URL is a valid YouTube link."""
    return any(pattern.match(url) for pattern in YOUTUBE_PATTERNS)

def get_user_input(use_template=False):  # Added use_template to skip extra input prompts
    """Gets the YouTube URL, output directory, quality, and format from the user."""
    url = get_valid_url_input("Enter the YouTube video/playlist URL: ")

    output_dir = get_output_directory()

    if not use_template:  # Only prompt for extra inputs if not using a template
        quality = get_valid_input("Enter desired quality (best/high/medium/low, default: best): ", ["best", "high", "medium", "low"], "best")
        format = get_valid_input("Enter desired format (mp4/webm/mp3, default: mp4): ", ["mp4", "webm", "mp3"], "mp4")
        download_subs = get_boolean_input("Download subtitles? (yes/no, default: no): ", "no")
    else:
        # Use template values
        quality, format, download_subs = "best", "mp4", False

    is_playlist = "playlist?list=" in url
    playlist_options = get_playlist_options(is_playlist)

    return url, output_dir, quality, format, is_playlist, download_subs, playlist_options

def get_valid_url_input(prompt: str) -> str:
    """Prompt user for a valid YouTube URL."""
    url = input(prompt)
    while not valid_youtube_link(url):
        print("Invalid YouTube URL. Please try again.")
        url = input(prompt)
    return url

def get_output_directory() -> str:
    """Prompt user for a valid output directory."""
    default_dir = "downloads"
    os.makedirs(default_dir, exist_ok=True)
    output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir
    while not os.path.isdir(output_dir) or not os.access(output_dir, os.W_OK):
        print("Invalid output directory or no write permissions. Please try again.")
        output_dir = input(f"Enter the output directory (default: {default_dir}): ") or default_dir
    return output_dir

def get_valid_input(prompt: str, valid_options: list, default: str) -> str:
    """Prompt user for a valid input, with a default option."""
    value = input(prompt) or default
    while value not in valid_options:
        print(f"Invalid input. Please choose from {valid_options}.")
        value = input(prompt)
    return value

def get_boolean_input(prompt: str, default: str) -> bool:
    """Prompt user for a yes/no answer and return True or False."""
    response = input(prompt).lower() or default
    return response == "yes"

def get_playlist_options(is_playlist: bool) -> dict:
    """Handles playlist-specific options if applicable."""
    playlist_options = {}
    if is_playlist:
        playlist_selection = input("Select specific videos? (yes/no, default: no): ").lower() or "no"
        if playlist_selection == "yes":
            while True:
                try:
                    playlist_options['playlist_items'] = input("Enter comma-separated video indices or ranges (e.g., 1,3,5-7): ")
                    break
                except ValueError:
                    print("Invalid input. Please enter comma-separated numbers or ranges.")
    return playlist_options
