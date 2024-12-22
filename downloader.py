import logging
import os
import urllib.error

from yt_dlp import YoutubeDL

def download_video(url: str, output_dir: str, quality: str, format: str, is_playlist: bool, download_subs: bool, playlist_options: dict):
    """Downloads the YouTube video/playlist with the specified quality and format."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ydl_opts = {
        'noplaylist': not is_playlist,  # Disable noplaylist if it's a playlist
        'nocheckcertificate': True,
        'format': get_format_selector(quality, format),
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'quiet': True,  # Suppress unnecessary terminal output
        'no_warnings': True,  # Suppress warnings
        'logtostderr': False,  # Disable error logging to stderr
        'writesubtitles': download_subs,  # Add the option to download subtitles
        'sub_lang': 'en',  # You can make this user-configurable later
        'sub_format': 'srt'  # You can make this user-configurable later
    }

    # Add playlist options if provided
    ydl_opts.update(playlist_options)

    try:
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl.download([url])
    except urllib.error.URLError as e:
        logging.error(f"Network error: {e}")
        print(f"Network error: {e}. Please check your internet connection.")
    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Download error: {e}")
        print(f"Download error: {e}. Please check the URL or try again later.")
    except yt_dlp.utils.PlaylistDownloadError as e:  # Handle playlist errors
        logging.error(f"Playlist download error: {e}")
        print(f"Playlist download error: {e}. Please check the playlist URL and video indices.")
    except FileNotFoundError as e:
        logging.error(f"File error: {e}")
        print(f"File error: {e}. Please check the output directory.")
    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

def get_format_selector(quality: str, format: str) -> str:
    """Returns the yt-dlp format selector string based on quality and format."""
    if quality == "best":
        quality_selector = "bv*+ba/b"
    elif quality == "high":
        quality_selector = "bv[height<=720]+ba/b"
    elif quality == "medium":
        quality_selector = "bv[height<=480]+ba/b"
    elif quality == "low":
        quality_selector = "bv[height<=360]+ba/b"
    else:
        quality_selector = "bv*+ba/b"  # Default to best

    if format == "mp3":
        return "ba"
    elif format in ("mp4", "webm"):
        return f"{quality_selector}[ext={format}]"
    else:
        return quality_selector  # Default to best

def progress_hook(d):
    """Progress hook for yt-dlp to display detailed download status."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes')
        speed = d.get('_speed_str')
        eta = d.get('_eta_str')

        progress = f"\rDownloading... {d.get('_percent_str', '0%')}"
        if total_bytes:
            progress += f" of {total_bytes_str(total_bytes)}"
        if speed:
            progress += f" at {speed}"
        if eta:
            progress += f" ETA {eta}"

        print(progress, end="")

    elif d['status'] == 'finished':
        print("\nDownload complete!")

    elif d['status'] == 'error':
        print("\nDownload failed!")

def total_bytes_str(total_bytes):
    """Converts bytes to a human-readable string."""
    if total_bytes < 1024:
        return f"{total_bytes}B"
    elif total_bytes < 1024 * 1024:
        return f"{total_bytes / 1024:.2f}KB"
    elif total_bytes < 1024 * 1024 * 1024:
        return f"{total_bytes / (1024 * 1024):.2f}MB"
    else:
        return f"{total_bytes / (1024 * 1024 * 1024):.2f}GB"
