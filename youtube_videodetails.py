import os
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
import re

# Scopes required for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Load the credentials from the token.json file
def load_credentials():
    if os.path.exists("token.json"):
        # Read the user's credentials from the token file
        return Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        raise Exception("Token file not found. Please authenticate first.")

# Initialize YouTube API client
def get_youtube_client():
    # Get the user's credentials and initialize the YouTube API client
    creds = load_credentials()
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=creds)
    return youtube

# Fetch video details 
def fetch_video_details(video_id):
    youtube = get_youtube_client()  # initialize the YouTube API client

    try:
        # Use the YouTube API to get details about the video
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        # If the video is found, get the details
        if "items" in response and len(response["items"]) > 0:
            video = response["items"][0]
            video_details = {
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "published_at": video["snippet"]["publishedAt"],
                "channel_title": video["snippet"]["channelTitle"],
                "view_count": video["statistics"].get("viewCount", "N/A")
            }
            return video_details
        else:
            print(f"Video with ID {video_id} not found.")
            return None
    except Exception as e:
        print(f"Error fetching video details: {e}")
        return None

# get the video ID from a YouTube URL
def extract_video_id(video_url):
    # Use regex to extract the video ID from the URL
    match = re.search(r"youtube\.com\/(?:watch\?v=|live\?v=)([A-Za-z0-9_-]+)", video_url)
    if match:
        return match.group(1)
    else:
        print("Invalid YouTube URL")
        return None



