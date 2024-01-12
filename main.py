import os
import pickle
import yt_dlp
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CREDENTIALS_PICKLE_PATH = "credentials.pickle"
CREDENTIALS_JSON_PATH = os.getenv("CREDENTIALS_JSON_PATH")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
VIDEO_FORMAT_ID = int(os.getenv("VIDEO_FORMAT_ID","22"))
PREFERRED_SUB_LANG_ID = os.getenv("PREFERRED_SUB_LANG_ID", "en")
VIDEO_SAVE_LOCATION = os.getenv("VIDEO_SAVE_LOCATION", "./downloads")

def load_credentials(credentials_path):
    credentials = None

    # Try to load credentials from pickle
    if os.path.exists(credentials_path):
        with open(credentials_path, "rb") as credentials_file:
            try:
                credentials = pickle.load(credentials_file)

                # Check if credentials are expired; if yes, reset them
                if credentials.expired:
                    credentials = None
            except (pickle.UnpicklingError, EOFError):
                pass

    return credentials

def save_credentials(credentials, credentials_path):
    with open(credentials_path, "wb") as credentials_file:
        pickle.dump(credentials, credentials_file)

def get_authenticated_service(credentials_path):
    credentials = load_credentials(credentials_path)

    # If credentials are not available or expired, get new ones
    if not credentials:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_JSON_PATH, ["https://www.googleapis.com/auth/youtube"])
        credentials = flow.run_local_server()

        # Save credentials for later use
        save_credentials(credentials, CREDENTIALS_PICKLE_PATH)

    # Create the YouTube service using the authenticated credentials
    youtube_service = build("youtube", "v3", credentials=credentials)

    return youtube_service

def get_video_ids_from_playlist(youtube, playlist_id):
    video_ids = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token,
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response["items"]:
            video_id = item["contentDetails"]["videoId"]
            video_ids.append(video_id)

        next_page_token = playlist_response.get("nextPageToken")

        if not next_page_token:
            break

    return video_ids

def download_video(video_id):
    ydl_opts = {
        'quiet': True,
        'format': f'{VIDEO_FORMAT_ID}',
        'outtmpl': os.path.join(VIDEO_SAVE_LOCATION, '%(title)s.%(ext)s'),
        'writesubtitles': True,
        'subtitleslangs': [PREFERRED_SUB_LANG_ID],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            return True
        except:
            return False

def remove_video_from_playlist(youtube, video_id):
    try:
        playlist_request = youtube.playlistItems().list(
            part="id",
            playlistId=PLAYLIST_ID,
            videoId=video_id
        )
        playlist_response = playlist_request.execute()

        if "items" in playlist_response and playlist_response["items"]:
            playlist_item_id = playlist_response["items"][0]["id"]

            response = youtube.playlistItems().delete(id=playlist_item_id).execute()
            print("\nDelete Response:", response)
            return True
        else:
            print(f"\nPlaylist item not found for video with ID '{video_id}'.")
            return False
    except Exception as e:
        print("\nAn error occurred while removing the video:", str(e))
        return False

def print_granted_scopes(credentials_path): 
    with open(credentials_path, "rb") as credentials_file:
        credentials = pickle.load(credentials_file)
        print("Granted Scopes:", credentials.scopes)

def list_videos_in_playlist(youtube, playlist_id):
    try:
        playlist_request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
        )
        playlist_response = playlist_request.execute()
        for item in playlist_response["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            video_title = item["snippet"]["title"]
            print(f"Video ID: {video_id}, Title: {video_title}")

    except Exception as e:
        print("\nAn error occurred:", str(e))

if __name__ == "__main__":
    # Create the YouTube service using the authenticated credentials
    youtube_service = get_authenticated_service(CREDENTIALS_PICKLE_PATH)
    print_granted_scopes(CREDENTIALS_PICKLE_PATH)
    print("\n")
    list_videos_in_playlist(youtube_service, PLAYLIST_ID)
    print("\n")

    # Get video IDs from the playlist
    video_ids = get_video_ids_from_playlist(youtube_service, PLAYLIST_ID)

    # Download and remove videos using yt-dlp
    for video_id in video_ids:
        if download_video(video_id):
            print(f"\nVideo with ID '{video_id}' downloaded successfully.")
            if remove_video_from_playlist(youtube_service, video_id):
                print(f"\nVideo with ID '{video_id}' removed from the playlist.")
            else:
                print(f"\nFailed to remove video with ID '{video_id}' from the playlist.")
        else:
            print(f"\nFailed to download video with ID '{video_id}'.")
    
