def compare_channels(
    first_channel_info,
    second_channel_info,
    first_analysis,
    second_analysis,
):
    first_subscribers = int(first_channel_info.get("subscribers", 0))
    second_subscribers = int(second_channel_info.get("subscribers", 0))

    first_views = int(first_channel_info.get("views", 0))
    second_views = int(second_channel_info.get("views", 0))

    first_videos = int(first_channel_info.get("videos", 0))
    second_videos = int(second_channel_info.get("videos", 0))

    first_average_views = float(first_analysis.get("average_views", 0))
    second_average_views = float(second_analysis.get("average_views", 0))

    first_average_likes = float(first_analysis.get("average_likes", 0))
    second_average_likes = float(second_analysis.get("average_likes", 0))

    first_average_comments = float(first_analysis.get("average_comments", 0))
    second_average_comments = float(second_analysis.get("average_comments", 0))

    first_name = first_channel_info.get("name", "Channel 1")
    second_name = second_channel_info.get("name", "Channel 2")

    return {
        "subscribers": {
            "first": first_subscribers,
            "second": second_subscribers,
            "winner": get_winner(first_subscribers, second_subscribers, first_name, second_name),
        },
        "total_views": {
            "first": first_views,
            "second": second_views,
            "winner": get_winner(first_views, second_views, first_name, second_name),
        },
        "video_count": {
            "first": first_videos,
            "second": second_videos,
            "winner": get_winner(first_videos, second_videos, first_name, second_name),
        },
        "average_views": {
            "first": first_average_views,
            "second": second_average_views,
            "winner": get_winner(first_average_views, second_average_views, first_name, second_name),
        },
        "average_likes": {
            "first": first_average_likes,
            "second": second_average_likes,
            "winner": get_winner(first_average_likes, second_average_likes, first_name, second_name),
        },
        "average_comments": {
            "first": first_average_comments,
            "second": second_average_comments,
            "winner": get_winner(first_average_comments, second_average_comments, first_name, second_name),
        },
    }


def get_winner(first_value, second_value, first_name, second_name):
    if first_value > second_value:
        return first_name

    if second_value > first_value:
        return second_name

    return "Tie"

def calculate_overall_winner(comparison):
    scores = {}

    for metric_data in comparison.values():
        winner = metric_data["winner"]

        if winner == "Tie":
            continue

        scores[winner] = scores.get(winner, 0) + 1

    if not scores:
        return {
            "scores": {},
            "winner": "Tie",
        }

    highest_score = max(scores.values())

    winners = [
        name
        for name, score in scores.items()
        if score == highest_score
    ]

    overall_winner = winners[0] if len(winners) == 1 else "Tie"

    return {
        "scores": scores,
        "winner": overall_winner,
    }