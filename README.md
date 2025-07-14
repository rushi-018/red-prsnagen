# Reddit User Persona Generator


This project takes a Reddit user profile URL, scrapes their posts & comments, and generates a structured, AI-powered user persona using Google's Gemini LLM.

---

## ✨ Features

* 🔗 Accepts any public Reddit user profile URL
* 🧹 Scrapes last 100 comments & 100 posts via Reddit API
* 🤖 Uses Gemini 2.5 Pro / 1.5 Flash to build a persona
* 📌 Includes **citations** from actual Reddit activity
* 📋 Displays a **clean, card-style persona** summary
* 📥 Allows download of the generated persona `.txt`
* 🌐 Built with **Streamlit** for a lightweight UI

---

## 🖥️ Live Interface Preview

![Screenshot](screenshot.png) <!-- Optional, if you upload -->

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env` File

Create a `.env` file in the root folder:

```env
CLIENT_ID=your_reddit_client_id
CLIENT_SECRET=your_reddit_client_secret
USER_AGENT=your_app_identifier
GEMINI_API_KEY=your_google_gemini_key
```

### 4. Run the Streamlit App

```bash
streamlit run streamlit_app.py
```

---

## 🧪 Sample Users

Try with:

```text
https://www.reddit.com/user/kojied/
https://www.reddit.com/user/Hungry-Move-6603/
```

It will generate `persona_kojied.txt` and display it in the UI.

---

## 🔄 Switching Between Gemini Models

You can select either model via dropdown:

* `gemini-2.5-pro` ✅ (Recommended: citations supported)
* `gemini-1.5-flash` ✅ (Free Tier)

---

## 📚 Notes for Evaluators

* Follows **PEP-8 guidelines**
* Clean, modular code (`reddit_scraper.py`, `persona_builder.py`, `run.py`, `streamlit_app.py`)
* Persona traits are parsed and shown neatly
* Codebase is extendable for future use cases

---

## 📎 Resources & API Setup

### 🔐 Reddit API Setup:

* Go to: [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
* Click “Create App” → type: `script`
* Redirect URI: `http://localhost:8080`
* Copy `client_id`, `client_secret`, `user_agent`

### 🔑 Gemini API Setup:

* Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
* Create a Google Cloud project and enable Gemini API
* Copy the API key to your `.env`

---

## 👨‍💻 Author

**Rushiraj Suwarnkar**

* 📬 [rushirajsuwarnkar018@gmail.com]
* 🌐 GitHub: https://github.com/rushi-018

---

## ✅ License

This project is only for the assignment evaluation. Code reuse only permitted if selected for internship.

---

## 🙌 Thank You

Thanks for the opportunity, BeyondChats! Looking forward to working together.
