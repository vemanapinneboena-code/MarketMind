import streamlit as st


def display_channel_information(info):
    st.divider()
    st.subheader("📊 Channel Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Subscribers",
            f"{int(info['subscribers']):,}"
        )

    with col2:
        st.metric(
            "Total Views",
            f"{int(info['views']):,}"
        )

    with col3:
        st.metric(
            "Videos",
            f"{int(info['videos']):,}"
        )

    st.write(f"**Channel Name:** {info['name']}")


def display_recent_videos(table):
    st.divider()
    st.subheader("🎬 Recent Videos")

    for index, row in enumerate(table, start=1):
        with st.expander(f"{index}. {row['Title']}"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Views", f"{row['Views']:,}")

            with col2:
                st.metric("Likes", f"{row['Likes']:,}")

            with col3:
                st.metric("Comments", f"{row['Comments']:,}")

            st.write(f"**Published:** {row['Published']}")


def display_performance_summary(analysis):
    st.divider()
    st.subheader("📈 Performance Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average Views",
            f"{analysis['average_views']:,.0f}"
        )

    with col2:
        st.metric(
            "Average Likes",
            f"{analysis['average_likes']:,.0f}"
        )

    with col3:
        st.metric(
            "Average Comments",
            f"{analysis['average_comments']:,.0f}"
        )

    top_video_views = 0

    if analysis["top_video"]:
        top_video_views = analysis["top_video"]["views"]

    with col4:
        st.metric(
            "Top Video Views",
            f"{top_video_views:,}"
        )


def display_top_video(analysis):
    if not analysis["top_video"]:
        return

    top_video = analysis["top_video"]

    st.success("🏆 Top Performing Video")
    st.write(f"**Title:** {top_video['title']}")
    st.write(f"**Views:** {top_video['views']:,}")
    st.write(f"**Likes:** {top_video['likes']:,}")
    st.write(f"**Comments:** {top_video['comments']:,}")


def display_keywords(keywords):
    st.divider()
    st.subheader("🔥 Top Keywords")

    for word, count in keywords:
        st.write(f"**{word}** — {count} videos")


def display_content_categories(topics):
    st.divider()
    st.subheader("📚 Content Categories")

    for topic, count in topics.items():
        st.write(f"**{topic}** — {count} videos")


def display_topic_performance(topic_performance):
    st.divider()
    st.subheader("🎯 Topic Performance")

    for topic, data in topic_performance.items():
        if data["videos"] == 0:
            continue

        with st.expander(f"{topic} — {data['videos']} videos"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Views",
                    f"{data['average_views']:,.0f}"
                )

            with col2:
                st.metric(
                    "Average Likes",
                    f"{data['average_likes']:,.0f}"
                )

            with col3:
                st.metric(
                    "Average Comments",
                    f"{data['average_comments']:,.0f}"
                )