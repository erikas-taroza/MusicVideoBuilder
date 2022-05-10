import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

privacyOptions = ("public", "unlisted", "private")

def get_service() -> Credentials:
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
    _privacy = int(input("Privacy (Public[0], Unlisted[1], Private[2]): "))

    _tags = []
    tags_file = open("./assets/config.txt", "r")
    tags_file_data = tags_file.readlines()[2:]
    for tag in tags_file_data:
        _tags.append(tag.strip())

    tags_file.close()

    input_tag = input("Tags (Press ENTER to add a new tag. Press ENTER on an empty line to stop.):\n").strip()
    while input_tag != "":
        if input_tag not in _tags:
            _tags.append(input_tag)
        input_tag = input("").strip()

    return dict(
        title = _title,
        description = _description,
        tags = _tags,
        privacy = _privacy
    )