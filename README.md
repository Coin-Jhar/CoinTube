# YouTube Downloader

A simple Python-based YouTube video downloader that allows you to download videos from YouTube in various formats and qualities. This project uses `yt-dlp`, a popular open-source tool for downloading videos from YouTube and many other websites.

## Features

- Download videos from YouTube using URLs.
- Select video format (`mp4`, `webm`, `mp3`).
- Choose video quality (`best`, `high`, `medium`, `low`).
- Save the downloaded videos to a specified directory.
- Error handling for common issues like invalid URLs or network problems.

## Installation

### Prerequisites

- Python 3.6 or higher
- `yt-dlp` library for downloading videos

### Install Dependencies

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/yourrepositoryname.git
   cd yourrepositoryname

2. Install the required dependencies:

pip install -r requirements.txt

If you don't have a requirements.txt, you can manually install yt-dlp:

pip install yt-dlp



## Usage

1. Run the main.py file:

python main.py


2. Follow the prompts in the terminal to input:

The YouTube video URL

The output directory (default: downloads)

Desired video quality (default: best)

Desired format (mp4, webm, or mp3; default: mp4)



3. The video will be downloaded and saved to the specified directory.



### Example

Here's an example of what the process looks like:

Enter the YouTube video URL: https://www.youtube.com/watch?v=example
Enter the output directory (default: downloads): my_videos
Enter desired quality (best/high/medium/low, default: best): best
Enter desired format (mp4/webm/mp3, default: mp4): mp4
Downloading... 50%
Downloading... 100%
Download complete! Check your output directory.

# Contributing

If you'd like to contribute to this project, feel free to fork the repository and create a pull request. Contributions are always welcome!

# License

This project is licensed under the MIT License - see the LICENSE file for details.