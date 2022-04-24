import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

privacyOptions = ("public", "unlisted", "private")

def get_service():
    try:
        creds: Credentials = None
        with open("./assets/credentials.pickle", "rb") as creds_file:
            creds = pickle.load(creds_file)

        if creds.expired:
            creds.refresh(Request())

        return build("youtube", "v3", credentials = creds)

    except FileNotFoundError:
        flow = InstalledAppFlow.from_client_secrets_file("./assets/client.json", ["https://www.googleapis.com/auth/youtube.upload"])
        creds = flow.run_local_server()

        creds_file = open("./assets/credentials.pickle", "wb")
        creds_file.write(pickle.dumps(creds))
        creds_file.close()

        return build("youtube", "v3", credentials = creds)

def upload_exported_video(video_path, args):
    request = dict(
        snippet = dict(
            title = args["title"],
            description = args["description"],
            tags = args["tags"],
        ),
        status = dict(
            privacyStatus = privacyOptions[args["privacy"]]
        )
    )

    video = MediaFileUpload(video_path)
    try:
        get_service().videos().insert(
            part = "snippet,status",
            body = request,
            media_body = video
        ).execute()
        print("Successfully uploaded video to YouTube.")
    except Exception as e:
        print("Error occurred when uploading to YouTube.")
        print(e)

def get_args() -> dict:
    print()
    _title = input("Title: ")
    _description = input("Description: ")
    _tags = input("Tags (tag1,tag2,tag3): ")
    _privacy = int(input("Privacy (Public[0], Unlisted[1], Private[2]): "))

    default_tags = open("./assets/tags.txt", "r").read()

    return dict(
        title = _title,
        description = _description,
        tags = (_tags + default_tags).split(","),
        privacy = _privacy
    )