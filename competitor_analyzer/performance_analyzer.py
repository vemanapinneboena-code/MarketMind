from competitor_analyzer.topic_classifier import TOPICS


def analyze_topic_performance(recent_videos, video_stats):
    topic_data = {
        topic: {
            "videos": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
        }
        for topic in TOPICS
    }

    for video in recent_videos:
        title = video["title"].lower()
        stats = video_stats.get(video["video_id"], {})

        for topic, keywords in TOPICS.items():
            matched = any(keyword in title for keyword in keywords)

            if matched:
                topic_data[topic]["videos"] += 1
                topic_data[topic]["total_views"] += stats.get("views", 0)
                topic_data[topic]["total_likes"] += stats.get("likes", 0)
                topic_data[topic]["total_comments"] += stats.get("comments", 0)

    results = {}

    for topic, data in topic_data.items():
        video_count = data["videos"]

        if video_count == 0:
            results[topic] = {
                "videos": 0,
                "average_views": 0,
                "average_likes": 0,
                "average_comments": 0,
            }
            continue

        results[topic] = {
            "videos": video_count,
            "average_views": data["total_views"] / video_count,
            "average_likes": data["total_likes"] / video_count,
            "average_comments": data["total_comments"] / video_count,
        }

    return results