TOPICS = {
    "Fundamental Analysis": [
        "pe",
        "peg",
        "roe",
        "roce",
        "opm",
        "margin",
        "profit",
        "balance",
        "sheet",
        "valuation",
    ],

    "Trading": [
        "trading",
        "intraday",
        "scalping",
        "option",
        "future",
        "time",
        "frames",
    ],

    "Market": [
        "nifty",
        "bank",
        "sensex",
        "stockmarket",
        "market",
    ],

    "Psychology": [
        "mindset",
        "emotion",
        "fear",
        "greed",
        "discipline",
    ],

    "Investment": [
        "invest",
        "portfolio",
        "sip",
        "mutual",
        "wealth",
    ]
}

def classify_topics(recent_videos):

    topic_count = {topic: 0 for topic in TOPICS}

    for video in recent_videos:

        title = video["title"].lower()

        for topic, keywords in TOPICS.items():

            for keyword in keywords:

                if keyword in title:
                    topic_count[topic] += 1
                    break

    return topic_count