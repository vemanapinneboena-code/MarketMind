def generate_ai_report(
    channel_info,
    analysis,
    topics,
    topic_performance,
    keywords
):
    channel_name = channel_info["name"]

    active_topics = {
        topic: count
        for topic, count in topics.items()
        if count > 0
    }

    dominant_topic = None

    if active_topics:
        dominant_topic = max(
            active_topics,
            key=active_topics.get
        )

    performing_topics = {
        topic: data
        for topic, data in topic_performance.items()
        if data["videos"] > 0
    }

    best_topic = None
    best_topic_data = None

    if performing_topics:
        best_topic = max(
            performing_topics,
            key=lambda topic: performing_topics[topic]["average_views"]
        )

        best_topic_data = performing_topics[best_topic]

    missing_topics = [
        topic
        for topic, count in topics.items()
        if count == 0
    ]

    top_keywords = [
        word
        for word, _ in keywords[:5]
    ]

    report_lines = []

    report_lines.append(f"Channel analyzed: {channel_name}.")
    report_lines.append(
        f"The recent videos average "
        f"{analysis['average_views']:,.0f} views, "
        f"{analysis['average_likes']:,.0f} likes, and "
        f"{analysis['average_comments']:,.0f} comments."
    )

    if dominant_topic:
        report_lines.append(
            f"The channel currently publishes most often about "
            f"{dominant_topic}."
        )

    if best_topic and best_topic_data:
        report_lines.append(
            f"{best_topic} is the strongest-performing topic, "
            f"with an average of "
            f"{best_topic_data['average_views']:,.0f} views per video."
        )

    if top_keywords:
        report_lines.append(
            "Frequently used title keywords include "
            + ", ".join(top_keywords)
            + "."
        )

    if missing_topics:
        report_lines.append(
            "The recent content contains little or no coverage of "
            + ", ".join(missing_topics)
            + "."
        )

    recommendations = []

    if best_topic:
        recommendations.append(
            f"Create more videos related to {best_topic}."
        )

    if missing_topics:
        recommendations.append(
            f"Test one or two videos about {missing_topics[0]} "
            "to evaluate audience interest."
        )

    if top_keywords:
        recommendations.append(
            f"Build follow-up videos around the keyword "
            f"'{top_keywords[0]}'."
        )

    return {
        "summary": report_lines,
        "recommendations": recommendations,
        "best_topic": best_topic,
        "dominant_topic": dominant_topic,
    }