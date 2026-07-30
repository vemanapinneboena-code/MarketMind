def analyze_videos(recent_videos, video_stats):

    if not recent_videos:
        return {
            "average_views": 0,
            "average_likes": 0,
            "average_comments": 0,
            "top_video": None
        }

    views = []
    likes = []
    comments = []

    for video in recent_videos:
        stats = video_stats.get(video["video_id"], {})

        views.append(stats.get("views", 0))
        likes.append(stats.get("likes", 0))
        comments.append(stats.get("comments", 0))

    top_video = max(
        recent_videos,
        key=lambda video: video_stats.get(
            video["video_id"], {}
        ).get("views", 0)
    )

    top_stats = video_stats.get(top_video["video_id"], {})

    return {
        "average_views": sum(views) / len(views),
        "average_likes": sum(likes) / len(likes),
        "average_comments": sum(comments) / len(comments),
        "top_video": {
            "title": top_video["title"],
            "views": top_stats.get("views", 0),
            "likes": top_stats.get("likes", 0),
            "comments": top_stats.get("comments", 0)
        }
    }