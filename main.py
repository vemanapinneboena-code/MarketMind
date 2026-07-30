from services.youtube_service import YouTubeService
from competitor_analyzer.channel_analyzer import analyze_videos


def main():
    youtube = YouTubeService()

    channel_name = input("Enter Channel Name: ").strip()

    channels = youtube.search_channel(channel_name)

    if len(channels) == 0:
        print("No channel found.")
        return

    print("\nChannels Found:\n")

    for index, channel in enumerate(channels, start=1):
        print(f"{index}. {channel['channel_name']}")

    try:
        choice = int(input("\nSelect Channel Number: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if choice < 1 or choice > len(channels):
        print("Invalid channel selection.")
        return

    selected = channels[choice - 1]

    info = youtube.get_channel_info(selected["channel_id"])

    recent_videos = youtube.get_recent_videos(
        selected["channel_id"],
        max_results=10
    )

    video_ids = [
        video["video_id"]
        for video in recent_videos
    ]

    video_stats = youtube.get_video_statistics(video_ids)
    analysis = analyze_videos(recent_videos, video_stats)

    views_list = [
        video_stats.get(video["video_id"], {}).get("views", 0)
        for video in recent_videos
    ]

    likes_list = [
        video_stats.get(video["video_id"], {}).get("likes", 0)
        for video in recent_videos
    ]

    comments_list = [
        video_stats.get(video["video_id"], {}).get("comments", 0)
        for video in recent_videos
    ]

    average_views = sum(views_list) / len(views_list) if views_list else 0
    average_likes = sum(likes_list) / len(likes_list) if likes_list else 0
    average_comments = sum(comments_list) / len(comments_list) if comments_list else 0

    best_video = max(
        recent_videos,
        key=lambda video: video_stats.get(
            video["video_id"], {}
        ).get("views", 0)
    )

    best_stats = video_stats.get(best_video["video_id"], {})

    print("\n========== PERFORMANCE SUMMARY ==========")
    print(f"Average Views    : {average_views:,.0f}")
    print(f"Average Likes    : {average_likes:,.0f}")
    print(f"Average Comments : {average_comments:,.0f}")
    print(f"Top Video        : {best_video['title']}")
    print(f"Top Video Views  : {best_stats.get('views', 0):,}")
    print("=========================================")

    print("\n========== CHANNEL INFORMATION ==========")
    print(f"Name         : {info['name']}")
    print(f"Subscribers  : {int(info['subscribers']):,}")
    print(f"Total Views  : {int(info['views']):,}")
    print(f"Videos       : {int(info['videos']):,}")
    print("=========================================")

    print("\nRecent Videos")
    print("-" * 60)

    for index, video in enumerate(recent_videos, start=1):
        stats = video_stats.get(video["video_id"], {})

        print(f"\n{index}. {video['title']}")
        print(f"   Published : {video['published_at']}")
        print(f"   Views     : {stats.get('views', 0):,}")
        print(f"   Likes     : {stats.get('likes', 0):,}")
        print(f"   Comments  : {stats.get('comments', 0):,}")

        print("\n========== PERFORMANCE SUMMARY ==========")
        print(f"Average Views    : {analysis['average_views']:,.0f}")
        print(f"Average Likes    : {analysis['average_likes']:,.0f}")
        print(f"Average Comments : {analysis['average_comments']:,.0f}")

        if analysis["top_video"]:
            print(f"Top Video        : {analysis['top_video']['title']}")
            print(f"Top Video Views  : {analysis['top_video']['views']:,}")

        print("=========================================")


if __name__ == "__main__":
    main()