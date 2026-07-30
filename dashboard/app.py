import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from services.youtube_service import YouTubeService
from services.channel_analysis_service import analyze_channel

from competitor_analyzer.comparison_analyzer import compare_channels
from dashboard.comparison_ui import display_comparison

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

st.subheader("Select Channels")

channel_name_1 = st.text_input(
    "Channel 1",
    placeholder="e.g. Fin Viraj",
)

channel_name_2 = st.text_input(
    "Channel 2",
    placeholder="e.g. CA Rachana Ranade",
)


# ---------------------------------------------------
# Analyze
# ---------------------------------------------------

if st.button("Analyze"):

    channel_name_1 = channel_name_1.strip()
    channel_name_2 = channel_name_2.strip()

    if not channel_name_1 or not channel_name_2:
        st.warning("Please enter both channel names.")
        st.stop()

    try:
        youtube = YouTubeService()

        with st.spinner("Searching YouTube..."):
            channels1 = youtube.search_channel(channel_name_1)
            channels2 = youtube.search_channel(channel_name_2)

        if not channels1:
            st.error("No matches found for Channel 1.")
            st.stop()

        if not channels2:
            st.error("No matches found for Channel 2.")
            st.stop()

        st.success(
            f"Found {len(channels1)} matches for Channel 1 and "
            f"{len(channels2)} matches for Channel 2."
        )

        selected_channel1 = st.selectbox(
            "Select Channel 1",
            channels1,
            format_func=lambda channel: channel["channel_name"],
        )

        selected_channel2 = st.selectbox(
            "Select Channel 2",
            channels2,
            format_func=lambda channel: channel["channel_name"],
        )

        with st.spinner("Analyzing both channels..."):
            channel1 = analyze_channel(
                channel_id=selected_channel1["channel_id"],
                max_results=10,
            )

            channel2 = analyze_channel(
                channel_id=selected_channel2["channel_id"],
                max_results=10,
            )
            comparison = compare_channels(
                channel1["info"],
                channel2["info"],
                channel1["analysis"],
                channel2["analysis"],
            )

        # ---------------------------------------------------
        # Temporary Dashboard
        # Displays Channel 1 using the current UI
        # ---------------------------------------------------

        info = channel1["info"]
        analysis = channel1["analysis"]
        keywords = channel1["keywords"]
        topics = channel1["topics"]
        topic_performance = channel1["topic_performance"]
        table = channel1["table"]
        ai_report = channel1["ai_report"]

        st.divider()
        st.header(
            f"Channel Analysis: {info.get('channel_name', 'Channel 1')}"
        )

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

        # ---------------------------------------------------
        # Channel Comparison
        # ---------------------------------------------------

        st.divider()

        display_comparison(comparison)

    except Exception as error:
        st.error("Something went wrong while analyzing the channels.")
        st.exception(error)