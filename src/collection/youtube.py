import os
from dotenv import load_dotenv
import googleapiclient.discovery

load_dotenv()
yt_api = os.environ.get("YOUTUBE_API_KEY")

api_service = "youtube"
api_version = "v3"

youtube = googleapiclient.discovery.build(
    api_service, api_version, developerKey=yt_api
)