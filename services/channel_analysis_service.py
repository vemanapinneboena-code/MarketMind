from services.youtube_service import YouTubeService
from competitor_analyzer.channel_analyzer import analyze_videos
from competitor_analyzer.content_analyzer import analyze_title_keywords
from competitor_analyzer.topic_classifier import classify_topics
from competitor_analyzer.performance_analyzer import analyze_topic_performance
from reports.ai_report import generate_ai_report


def analyze_channel(channel_id, max_results=10):
    youtube = YouTubeService()

    info = youtube.get_channel_info(channel_id)

    recent_videos = youtube.get_recent_videos(
        channel_id,
        max_results=max_results,
    )

    video_ids = [
        video["video_id"]
        for video in recent_videos
    ]

    video_stats = youtube.get_video_statistics(video_ids)

    analysis = analyze_videos(
        recent_videos,
        video_stats,
    )

    keywords = analyze_title_keywords(recent_videos)

    topics = classify_topics(recent_videos)

    topic_performance = analyze_topic_performance(
        recent_videos,
        video_stats,
    )

    ai_report = generate_ai_report(
        channel_info=info,
        analysis=analysis,
        topics=topics,
        topic_performance=topic_performance,
        keywords=keywords,
    )

    table = []

    for video in recent_videos:
        stats = video_stats.get(video["video_id"], {})

        table.append(
            {
                "Title": video["title"],
                "Published": video["published_at"][:10],
                "Views": stats.get("views", 0),
                "Likes": stats.get("likes", 0),
                "Comments": stats.get("comments", 0),
            }
        )

    return {
        "info": info,
        "videos": recent_videos,
        "video_stats": video_stats,
        "analysis": analysis,
        "keywords": keywords,
        "topics": topics,
        "topic_performance": topic_performance,
        "table": table,
        "ai_report": ai_report,
    }