import os, sys, json, requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

video_path = sys.argv[1]
title = sys.argv[2]
desc = sys.argv[3]

CLIENT_ID = os.environ["YT_CLIENT_ID"]
CLIENT_SECRET = os.environ["YT_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["YT_REFRESH_TOKEN"]

# گرفتن access_token با refresh_token
resp = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    },
    timeout=30,
)
resp.raise_for_status()
access_token = resp.json()["access_token"]

creds = Credentials(
    token=access_token,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
)

youtube = build("youtube", "v3", credentials=creds)

body = {
    "snippet": {
        "title": title,
        "description": desc,
        "tags": ["Tech","AI","Shorts"]
    },
    "status": { "privacyStatus": "public" }
}

media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Uploaded {int(status.progress()*100)}%")
print("Upload complete:", json.dumps(response, ensure_ascii=False)[:500])
