# streamlit_app.py
import streamlit as st
import os
import json
import google.generativeai as genai
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_AGENT")
)

# Streamlit config
st.set_page_config(page_title="Reddit Persona Generator", layout="centered")
st.title("🧠 Reddit Persona Generator")
st.markdown("""
Generate a concise, citation-rich Reddit user persona from a profile URL.
""")

# Input Reddit URL
url = st.text_input("🔗 Reddit Profile URL", "https://www.reddit.com/user/kojied/")
model_choice = st.selectbox("🤖 Choose Gemini Model", ["gemini-2.5-pro", "gemini-1.5-flash"])

if st.button("✨ Generate Persona"):
    username = url.rstrip("/").split("/")[-1]
    gemini_model = genai.GenerativeModel(model_choice)

    with st.spinner("🔍 Scraping Reddit activity..."):
        redditor = reddit.redditor(username)
        data = {"username": username, "comments": [], "posts": []}

        try:
            for c in redditor.comments.new(limit=100):
                data["comments"].append({
                    "body": c.body,
                    "subreddit": str(c.subreddit),
                    "permalink": f"https://www.reddit.com{c.permalink}"
                })
            for p in redditor.submissions.new(limit=100):
                data["posts"].append({
                    "title": p.title,
                    "selftext": p.selftext,
                    "subreddit": str(p.subreddit),
                    "permalink": f"https://www.reddit.com{p.permalink}"
                })
        except Exception as e:
            st.error(f"Reddit scraping failed: {e}")
            st.stop()

    # Build prompt
    all_content = []
    for p in data["posts"][:30]:
        all_content.append(f"Post Title: {p['title']}\nBody: {p['selftext']}\nSubreddit: {p['subreddit']}\nLink: {p['permalink']}")
    for c in data["comments"][:30]:
        all_content.append(f"Comment: {c['body']}\nSubreddit: {c['subreddit']}\nLink: {c['permalink']}")
    content = "\n---\n".join(all_content)

    prompt = f"""
You are an AI that creates user personas based on Reddit data.
Respond ONLY with the persona. No intros or explanations. Format should be structured and concise:

Persona Template:
- **Name**:
- **Age Range**:
- **Occupation**:
- **Interests & Hobbies**:
- **Personality Traits**:
- **Writing Style**:
- **Emotional Tone**:
- **Humor Style**:
- **Political Views**:
- **Mental Health Clues**:
- **Favorite Subreddits**:

📌 For each trait, cite the exact Reddit comment/post with subreddit + link.

Here’s the user activity:
{content}
"""

    with st.spinner("🧠 Generating Persona with Gemini..."):
        try:
            response = gemini_model.generate_content(prompt)
            persona_text = response.text.strip()

            # Remove any filler like "Here's what I found"
            start_idx = persona_text.lower().find("- **name**")
            persona_clean = persona_text[start_idx:] if start_idx != -1 else persona_text

            # Save
            out_file = f"persona_{username}.txt"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(persona_clean)

            st.success("✅ Persona generated!")
            st.download_button("📥 Download Persona", persona_clean, file_name=out_file)

            st.subheader("🧬 Persona Card")
            for line in persona_clean.split("\n"):
                if line.startswith("- **"):
                    trait, value = line.replace("- ", "").split(":", 1)
                    st.markdown(f"**{trait.strip()}**: {value.strip()}")

            st.markdown("---")
            st.markdown("<h4>📄 Full Persona with Citations:</h4>", unsafe_allow_html=True)
            st.code(persona_clean)

        except Exception as e:
            st.error(f"Gemini generation failed: {e}")
