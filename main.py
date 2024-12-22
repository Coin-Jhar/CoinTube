import json
import logging

from downloader import download_video
from utils import get_user_input


def load_config(config_file):
    """Loads the configuration from the specified JSON file."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Configuration file not found: {config_file}")
        return None
    except json.JSONDecodeError:
        print(f"Error parsing configuration file: {config_file}")
        return None

def select_template(config):
    """Presents the available templates to the user and gets their selection."""
    if config and "templates" in config:
        templates = config["templates"]
        print("Available templates:")
        for i, template_name in enumerate(templates):
            print(f"{i+1}. {template_name}")

        while True:
            try:
                choice = int(input("Select a template (enter number): "))
                if 1 <= choice <= len(templates):
                    selected_template = list(templates.keys())[choice - 1]
                    return templates[selected_template]
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    else:
        print("No templates found in the configuration file.")
        return None

if __name__ == "__main__":
    logging.basicConfig(filename='downloader.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    config = load_config("config.json")  # Load the configuration
    template = select_template(config)  # Let the user select a template

    if template:
        # Pass use_template=True to skip prompts in get_user_input()
        video_url, output_directory, _, _, is_playlist, _, playlist_options = get_user_input(use_template=True)  

        try:
            download_video(
                video_url,
                output_directory,
                template.get("quality", "best"),  # Use template or default values
                template.get("format", "mp4"),
                is_playlist,
                template.get("download_subs", False),
                playlist_options
            )
            print("Download complete! Check your output directory.")
        except Exception as e:
            logging.error(f"Failed to download video: {e}")
            print("An error occurred while downloading the video. Check the logs for details.")
