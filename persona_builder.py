import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini Pro model
model = genai.GenerativeModel("gemini-2.5-pro")

def read_activity_file(username):
    with open(f"{username}_activity.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_prompt(data):
    posts = data.get("posts", [])
    comments = data.get("comments", [])
    
    all_texts = []

    for p in posts:
        text = f"Post Title: {p['title']}\nBody: {p['selftext']}\nSubreddit: {p['subreddit']}\nLink: {p['permalink']}\n---"
        all_texts.append(text)

    for c in comments:
        text = f"Comment: {c['body']}\nSubreddit: {c['subreddit']}\nLink: {c['permalink']}\n---"
        all_texts.append(text)

    activity_text = "\n".join(all_texts[:50])  # Limit to avoid token overflow

    prompt = f"""
You are an AI assistant tasked with analyzing Reddit activity to build a detailed **User Persona**.

Analyze the user's Reddit posts and comments below, and generate a well-structured persona using these traits:

- Possible Name
- Age Range
- Occupation/Field
- Personality Traits
- Interests/Hobbies
- Writing Tone
- Political/Worldview (if any)
- Sentiment and emotional tone
- Favorite Subreddits
- Mental health mentions
- Humor Style
- Any self-disclosed personal experiences
- Language Style (formal, casual, sarcastic, etc.)

📌 IMPORTANT: For each trait, include the exact post/comment (with subreddit and link) that helped you infer it.

Here’s the user’s activity:
{activity_text}
"""
    return prompt

def generate_persona(username):
    data = read_activity_file(username)
    prompt = build_prompt(data)

    print("🤖 Sending prompt to Gemini...")
    response = model.generate_content(prompt)

    # Save output
    out_file = f"persona_{username}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"✅ Persona saved to {out_file}")

if __name__ == "__main__":
    profile_url = input("Enter Reddit profile URL: ").strip()
    if profile_url.endswith("/"):
        profile_url = profile_url[:-1]
    username = profile_url.split("/")[-1]

    generate_persona(username)
