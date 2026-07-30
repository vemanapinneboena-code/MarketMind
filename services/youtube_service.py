import os
import html

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()


class YouTubeService:

    def __init__(self):
        api_key = os.getenv("YOUTUBE_API_KEY")

        if not api_key:
            raise ValueError("YOUTUBE_API_KEY not found.")

        self.youtube = build(
            "youtube",
            "v3",
            developerKey=api_key
        )

    def search_channel(self, channel_name):

        request = self.youtube.search().list(
            part="snippet",
            q=channel_name,
            type="channel",
            maxResults=5
        )

        response = request.execute()

        channels = []

        for item in response["items"]:
            channels.append({
                "channel_name": item["snippet"]["title"],
                "channel_id": item["snippet"]["channelId"]
            })

        return channels

    def get_channel_info(self, channel_id):

        request = self.youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )

        response = request.execute()

        if len(response["items"]) == 0:
            return None

        item = response["items"][0]

        return {
            "name": item["snippet"]["title"],
            "subscribers": item["statistics"].get("subscriberCount", "0"),
            "views": item["statistics"].get("viewCount", "0"),
            "videos": item["statistics"].get("videoCount", "0")
        }

    def get_recent_videos(self, channel_id, max_results=10):

        request = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            order="date",
            type="video",
            maxResults=max_results
        )

        response = request.execute()

        videos = []

        for item in response.get("items", []):
            videos.append({
                "video_id": item["id"]["videoId"],
                "title": html.unescape(item["snippet"]["title"]),
                "published_at": item["snippet"]["publishedAt"]
            })

        return videos

    def get_video_statistics(self, video_ids):

        request = self.youtube.videos().list(
            part="statistics",
            id=",".join(video_ids)
        )

        response = request.execute()

        stats = {}

        for item in response.get("items", []):
            stats[item["id"]] = {
                "views": int(item["statistics"].get("viewCount", 0)),
                "likes": int(item["statistics"].get("likeCount", 0)),
                "comments": int(item["statistics"].get("commentCount", 0))
            }

        return stats