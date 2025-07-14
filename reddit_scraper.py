import os
import praw
from dotenv import load_dotenv
import json

load_dotenv()

# Load credentials from .env
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
user_agent = os.getenv("USER_AGENT")

# Authenticate
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

def scrape_user(username):
    redditor = reddit.redditor(username)

    data = {
        "username": username,
        "comments": [],
        "posts": []
    }

    print(f"🔍 Scraping comments for u/{username}...")
    try:
        for comment in redditor.comments.new(limit=100):
            data["comments"].append({
                "body": comment.body,
                "score": comment.score,
                "created_utc": comment.created_utc,
                "permalink": f"https://www.reddit.com{comment.permalink}",
                "subreddit": str(comment.subreddit)
            })
    except Exception as e:
        print("⚠️ Error while fetching comments:", e)

    print(f"🔍 Scraping posts for u/{username}...")
    try:
        for post in redditor.submissions.new(limit=100):
            data["posts"].append({
                "title": post.title,
                "selftext": post.selftext,
                "score": post.score,
                "created_utc": post.created_utc,
                "url": post.url,
                "permalink": f"https://www.reddit.com{post.permalink}",
                "subreddit": str(post.subreddit)
            })
    except Exception as e:
        print("⚠️ Error while fetching posts:", e)

    # Save to file
    with open(f"{username}_activity.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Data saved to {username}_activity.json")

if __name__ == "__main__":
    user_url = input("Enter Reddit profile URL: ").strip()
    if user_url.endswith("/"):
        user_url = user_url[:-1]
    username = user_url.split("/")[-1]
    scrape_user(username)
