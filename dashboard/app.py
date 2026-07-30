import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from services.youtube_service import YouTubeService
from competitor_analyzer.channel_analyzer import analyze_videos
from competitor_analyzer.content_analyzer import analyze_title_keywords
from competitor_analyzer.topic_classifier import classify_topics
from competitor_analyzer.performance_analyzer import analyze_topic_performance
from reports.ai_report import generate_ai_report

from ui import (
    display_channel_information,
    display_recent_videos,
    display_performance_summary,
    display_top_video,
    display_keywords,
    display_content_categories,
    display_topic_performance,
)


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="MarketMind",
    page_icon="📈",
    layout="wide",
)

st.title("📈 MarketMind")
st.subheader("AI Powered YouTube Competitor Analyzer")


# ---------------------------------------------------
# User Input
# ---------------------------------------------------

channel_name = st.text_input("Enter Channel Name")


# ---------------------------------------------------
# Analyze
# ---------------------------------------------------

if st.button("Analyze"):

    channel_name = channel_name.strip()

    if not channel_name:
        st.warning("Please enter a channel name.")
        st.stop()

    try:
        youtube = YouTubeService()

        with st.spinner("Searching YouTube..."):
            channels = youtube.search_channel(channel_name)

        if not channels:
            st.error("No channel found.")
            st.stop()

        st.success(f"Found {len(channels)} matching channels.")

        selected_channel = st.selectbox(
            "Select a Channel",
            channels,
            format_func=lambda channel: channel["channel_name"],
        )

        channel_id = selected_channel["channel_id"]

        with st.spinner("Analyzing channel..."):
            info = youtube.get_channel_info(channel_id)

            recent_videos = youtube.get_recent_videos(
                channel_id,
                max_results=10,
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

        # ---------------------------------------------------
        # Dashboard Sections
        # ---------------------------------------------------

        display_channel_information(info)
        display_recent_videos(table)
        display_performance_summary(analysis)
        display_top_video(analysis)
        display_keywords(keywords)
        display_content_categories(topics)
        display_topic_performance(topic_performance)

        # ---------------------------------------------------
        # AI Competitor Report
        # ---------------------------------------------------

        st.divider()
        st.subheader("🤖 AI Competitor Report")

        for paragraph in ai_report["summary"]:
            st.write(paragraph)

        st.markdown("### Recommendations")

        for recommendation in ai_report["recommendations"]:
            st.write(f"✅ {recommendation}")

    except Exception as error:
        st.error("Something went wrong while analyzing the channel.")
        st.exception(error)