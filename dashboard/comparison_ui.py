import streamlit as st


def format_number(value):
    value = float(value)

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if value >= 1_000:
        return f"{value / 1_000:.1f}K"

    if value.is_integer():
        return f"{int(value):,}"

    return f"{value:,.1f}"


def display_comparison(
    comparison,
    first_name,
    second_name,
    overall_result,
):
    st.divider()
    st.header("⚔️ Channel Comparison")

    st.markdown(
        f"### {first_name}  **VS**  {second_name}"
    )

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
            st.metric(
                first_name,
                format_number(data["first"]),
            )

        with col2:
            st.metric(
                second_name,
                format_number(data["second"]),
            )

        with col3:
            st.success(f"🏆 {data['winner']}")

    st.divider()
    st.subheader("🏁 Overall Score")

    first_score = overall_result["scores"].get(first_name, 0)
    second_score = overall_result["scores"].get(second_name, 0)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(first_name, first_score)

    with col2:
        st.metric(second_name, second_score)

    overall_winner = overall_result["winner"]

    if overall_winner == "Tie":
        st.info("Overall result: Tie")
    else:
        st.success(f"🏆 Overall Winner: {overall_winner}")

    st.caption(
        "One point is awarded for each metric won. "
        "This is a simple comparison score, not an absolute "
        "judgment of channel quality."
    )