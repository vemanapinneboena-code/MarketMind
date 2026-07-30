import streamlit as st


def display_comparison(comparison):
    st.divider()
    st.header("⚔️ Channel Comparison")

    metrics = [
        ("Subscribers", "subscribers"),
        ("Total Views", "total_views"),
        ("Videos", "video_count"),
        ("Average Views", "average_views"),
        ("Average Likes", "average_likes"),
        ("Average Comments", "average_comments"),
    ]

    for title, key in metrics:
        data = comparison[key]

        st.subheader(title)

        col1, col2, col3 = st.columns([3, 3, 2])

        with col1:
            st.metric("Channel 1", f"{data['first']:,}")

        with col2:
            st.metric("Channel 2", f"{data['second']:,}")

        with col3:
            st.success(f"🏆 {data['winner']}")