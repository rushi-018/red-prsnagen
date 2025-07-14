import os
import json
import praw
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Setup credentials
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")  # You can switch to 1.5-flash if needed

def scrape_user(username):
    redditor = reddit.redditor(username)
    data = {
        "username": username,
        "comments": [],
        "posts": []
    }

    for comment in redditor.comments.new(limit=100):
        data["comments"].append({
            "body": comment.body,
            "permalink": f"https://www.reddit.com{comment.permalink}",
            "subreddit": str(comment.subreddit)
        })

    for post in redditor.submissions.new(limit=100):
        data["posts"].append({
            "title": post.title,
            "selftext": post.selftext,
            "permalink": f"https://www.reddit.com{post.permalink}",
            "subreddit": str(post.subreddit)
        })

    with open(f"{username}_activity.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return data

def build_prompt(data):
    parts = []

    for p in data['posts'][:30]:
        parts.append(f"Post Title: {p['title']}\nPost Body: {p['selftext']}\nSubreddit: {p['subreddit']}\nLink: {p['permalink']}\n---")

    for c in data['comments'][:30]:
        parts.append(f"Comment: {c['body']}\nSubreddit: {c['subreddit']}\nLink: {c['permalink']}\n---")

    joined = "\n".join(parts)
    return f"""
You're an AI that creates user personas based on Reddit activity.

Generate a detailed persona using:
- Name (if guessable)
- Age range
- Occupation or student status
- Interests/hobbies
- Political/ideological views (if any)
- Emotional tone
- Writing style
- Mental health clues (if any)
- Humor type
- Favorite subreddits

📌 For each trait, include citations: exact comments or post links you used.

Here is the user's activity:
{joined}
"""

def generate_persona(username):
    with open(f"{username}_activity.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    prompt = build_prompt(data)
    response = model.generate_content(prompt)
    with open(f"persona_{username}.txt", "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"✅ Persona saved to persona_{username}.txt")

if __name__ == "__main__":
    url = input("Enter Reddit profile URL: ").strip()
    username = url.rstrip("/").split("/")[-1]
    print("🔍 Scraping...")
    scrape_user(username)
    print("🧠 Generating persona...")
    generate_persona(username)
    print("🎯 All done.")
