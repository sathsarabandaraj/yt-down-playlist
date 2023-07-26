# yt-down-playlist

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
