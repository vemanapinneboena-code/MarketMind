import re


TOPICS = {
    "Fundamental Analysis": [
        "pe ratio",
        "peg ratio",
        "roe",
        "roce",
        "opm",
        "operating profit margin",
        "valuation",
        "balance sheet",
        "promoter holding",
        "pledged shares",
        "fundamental analysis",
    ],

    "Trading": [
        "trading",
        "intraday",
        "scalping",
        "option trading",
        "option selling",
        "futures",
        "technical analysis",
        "time frames",
        "trader",
    ],

    "Market": [
        "nifty",
        "bank nifty",
        "sensex",
        "stock market",
        "stockmarket",
        "market crash",
        "market analysis",
    ],

    "Psychology": [
        "mindset",
        "emotion",
        "fear",
        "greed",
        "discipline",
        "trading psychology",
        "loss psychology",
    ],

    "Investment": [
        "investing",
        "investment",
        "portfolio",
        "sip",
        "mutual fund",
        "wealth creation",
        "long term",
    ],
}


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_keyword(text, keyword):
    normalized_keyword = normalize_text(keyword)

    if " " in normalized_keyword:
        return normalized_keyword in text

    pattern = rf"\b{re.escape(normalized_keyword)}\b"
    return re.search(pattern, text) is not None


def classify_video(title):
    normalized_title = normalize_text(title)

    matched_topics = []

    for topic, keywords in TOPICS.items():
        if any(
            contains_keyword(normalized_title, keyword)
            for keyword in keywords
        ):
            matched_topics.append(topic)

    if not matched_topics:
        return ["Other"]

    return matched_topics


def classify_topics(recent_videos):
    topic_count = {
        topic: 0
        for topic in TOPICS
    }

    topic_count["Other"] = 0

    for video in recent_videos:
        matched_topics = classify_video(video["title"])

        for topic in matched_topics:
            topic_count[topic] += 1

    return topic_count