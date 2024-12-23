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

def get_user_input(use_template=False, template=None):
    """
    Gets the YouTube URL, output directory, quality, and format from the user.
    Supports using predefined templates for automation.

    Args:
        use_template (bool): Whether to use predefined template values.
        template (dict): The template containing default values (if applicable).

    Returns:
        tuple: (url, output_dir, quality, format, is_playlist, download_subs, playlist_options)
    """
    url = input("Enter the YouTube video/playlist URL: ").strip()

    while not valid_youtube_link(url):
        print("Invalid YouTube URL. Please try again.")
        url = input("Enter the YouTube video/playlist URL: ").strip()

    default_dir = "downloads"
    os.makedirs(default_dir, exist_ok=True)

    output_dir = (
        template.get("output_dir", default_dir)
        if use_template and template
        else input(f"Enter the output directory (default: {default_dir}): ").strip() or default_dir
    )

    while not os.path.isdir(output_dir) or not os.access(output_dir, os.W_OK):
        print("Invalid output directory or no write permissions. Please try again.")
        output_dir = input(f"Enter the output directory (default: {default_dir}): ").strip() or default_dir

    valid_qualities = ["best", "high", "medium", "low"]
    quality = (
        template.get("quality", "best")
        if use_template and template
        else input("Enter desired quality (best/high/medium/low, default: best): ").strip() or "best"
    )
    while quality not in valid_qualities:
        print(f"Invalid quality. Please choose from {valid_qualities}.")
        quality = input("Enter desired quality: ").strip()

    valid_formats = ["mp4", "webm", "mp3"]
    format = (
        template.get("format", "mp4")
        if use_template and template
        else input("Enter desired format (mp4/webm/mp3, default: mp4): ").strip() or "mp4"
    )
    while format not in valid_formats:
        print(f"Invalid format. Please choose from {valid_formats}.")
        format = input("Enter desired format: ").strip()

    download_subs = (
        template.get("download_subs", False)
        if use_template and template
        else input("Download subtitles? (yes/no, default: no): ").strip().lower() == "yes"
    )

    is_playlist = "playlist?list=" in url  # Basic playlist detection
    playlist_options = {}
    if is_playlist:
        playlist_selection = input("Select specific videos? (yes/no, default: no): ").strip().lower() or "no"
        if playlist_selection == "yes":
            while True:
                try:
                    playlist_options['playlist_items'] = input(
                        "Enter comma-separated video indices or ranges (e.g., 1,3,5-7): "
                    ).strip()
                    break  # Exit loop if input is valid
                except ValueError:
                    print("Invalid input. Please enter comma-separated numbers or ranges.")

    return url, output_dir, quality, format, is_playlist, download_subs, playlist_options
