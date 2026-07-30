from collections import Counter
import re


STOP_WORDS = {
    "the", "is", "in", "on", "of", "for",
    "and", "to", "how", "what", "with",
    "a", "an", "your", "this", "that",
    "telugu", "finviraj"
}


def analyze_title_keywords(recent_videos):

    words = []

    for video in recent_videos:

        title = video["title"].lower()

        title = re.sub(r"[^a-zA-Z0-9 ]", " ", title)

        for word in title.split():

            if len(word) < 3:
                continue

            if word in STOP_WORDS:
                continue

            words.append(word)

    counter = Counter(words)

    return counter.most_common(10)