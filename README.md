# yt-down-playlist
## ⚠ Warning
> This script will delete the video from the playlist after download is finished.
> You can always remove the functionality by commenting out the following code snippet from the `your_script.py`.
>
>```python
>      if remove_video_from_playlist(youtube_service, video_id):
>        print(f"\nVideo with ID '{video_id}' removed from the playlist.")
>      else:
>        print(f"\nFailed to remove video with ID '{video_id}' from the playlist.")
>```

## Introduction

Download Youtube videos from specific playlist using yt-dlp

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/your-repo.git`
2. Change into the project directory: `cd your-repo`

## Setup

1. Create a Google Cloud project and enable the YouTube Data API v3.
2. Obtain the necessary credentials to access the API (API key or OAuth 2.0 credentials).
3. Rename `.env.example` to `.env` and fill in your API key, credentials and playlist id.

## Requirements

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Python script:

```bash
python your_script.py
```

## Notes

- Make sure you have proper authorization to access the private playlist.
- Protect your .env file and never share it, especially when containing sensitive data like API keys.
