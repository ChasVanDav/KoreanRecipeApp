import os
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials

# Path to your client_secrets.json file
CLIENT_SECRETS_FILE = "client_secrets.json"

# Scopes required for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def authenticate_youtube_api():
    creds = None

    # Check if there is a saved token from previous authentication
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            if creds and creds.valid:
                print("Using existing credentials...")
                return creds
            elif creds and creds.expired and creds.refresh_token:
                # Token has expired, but can be refreshed using the refresh token
                creds.refresh(Request())
                print("Token refreshed successfully.")
                # Save the refreshed token for future use
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
                return creds
            else:
                print("Credentials are invalid. Re-authenticating...")
                creds = None
        except Exception as e:
            print(f"Error loading token: {e}")
            creds = None

    # If no valid credentials, initiate the OAuth login flow
    if not creds:
        print("No valid credentials found, starting OAuth flow...")
        try:
            # Create the OAuth flow using the client_secrets.json file
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)  # Local server to handle the OAuth callback

            # Authentication successful, save the credentials for future use
            with open("token.json", "w") as token:
                token.write(creds.to_json())
            print("Authentication successful, credentials saved.")

        except Exception as e:
            print(f"Error during OAuth flow: {e}")
            raise

    return creds

# Call the authentication function
if __name__ == "__main__":
    authenticate_youtube_api()
