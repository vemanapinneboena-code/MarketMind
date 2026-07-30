import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from services.youtube_service import YouTubeService
from services.channel_analysis_service import analyze_channel

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
            result = analyze_channel(
                channel_id=channel_id,
                max_results=10,
            )

        info = result["info"]
        analysis = result["analysis"]
        keywords = result["keywords"]
        topics = result["topics"]
        topic_performance = result["topic_performance"]
        table = result["table"]
        ai_report = result["ai_report"]

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

        for paragraph in ai_report.get("summary", []):
            st.write(paragraph)

        st.markdown("### Recommendations")

        recommendations = ai_report.get("recommendations", [])

        if recommendations:
            for recommendation in recommendations:
                st.write(f"✅ {recommendation}")
        else:
            st.info("No recommendations were generated.")

    except Exception as error:
        st.error("Something went wrong while analyzing the channel.")
        st.exception(error)