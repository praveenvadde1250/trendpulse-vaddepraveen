
import requests
import time
import json
import os
from datetime import datetime

# ---------------------------------------------
# CONFIGURATION
# ---------------------------------------------

BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}
MAX_STORIES_PER_CATEGORY = 25

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------

def fetch_top_story_ids():
    try:
        url = f"{BASE_URL}/topstories.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def fetch_story_details(story_id):
    try:
        url = f"{BASE_URL}/item/{story_id}.json"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def assign_category(title):
    if not title:
        return None

    title = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title:
                return category

    return None


# ---------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------

def main():
    story_ids = fetch_top_story_ids()

    if not story_ids:
        print("No stories fetched. Exiting...")
        return

    collected_stories = []
    category_count = {cat: 0 for cat in CATEGORIES}

    # Loop through each category
    for category in CATEGORIES:
        print(f"Processing category: {category}")

        for story_id in story_ids:

            if category_count[category] >= MAX_STORIES_PER_CATEGORY:
                break

            story = fetch_story_details(story_id)

            if not story:
                continue

            title = story.get("title", "")
            detected_category = assign_category(title)

            if detected_category == category:

                story_data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_stories.append(story_data)
                category_count[category] += 1

        # Required delay after each category
        time.sleep(2)

    # ---------------------------------------------
    # SAVE TO JSON
    # ---------------------------------------------

    os.makedirs("data", exist_ok=True)

    today_str = datetime.now().strftime('%Y%m%d')
    filename = f"data/trends_{today_str}.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(collected_stories, file, indent=4)

    # ---------------------------------------------
    # FINAL OUTPUT (MATCHES REQUIREMENT EXACTLY)
    # ---------------------------------------------

    print(f"Collected {len(collected_stories)} stories. Saved to {filename}")


# ---------------------------------------------
# RUN SCRIPT
# ---------------------------------------------

if __name__ == "__main__":
    main()