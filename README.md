# 🧠 Sith StudyFlow - AI-Powered Productivity Companion

Welcome to **Sith StudyFlow**, a Streamlit-powered productivity dashboard infused with the power of **Groq AI** and **Darth Sidious-inspired UI**. Whether you're planning your tasks, chatting with your AI assistant, or listening to mood-based music, this tool brings AI and organization into perfect harmony.

---

## 🧩 Problem Statement

As a student, I was frustrated switching between:
- 🎧 Spotify for music,
- 📝 Excel/Notion for schedules and task tracking,
- 🤖 ChatGPT for help with questions.

So I decided to **combine all three** into a **single app** that integrates:
> 🎶 Mood-based music + 🗓️ Productivity planner + 🤖 AI assistant

This is a **basic prototype** built during a hackathon and can be **scaled significantly** in the future.

> ⚠️ **Note:** Only limited local music tracks are included for now.  
Spotify API integration was attempted but not completed in time.

---

## 🌟 Features

### 1. 🤖 AI Chatbot (Groq API Powered)
- Chat with an LLM assistant using **Groq’s blazing-fast API**.
- Memory-enabled session: remembers previous messages.
- Session manager: rename, delete, and export chat logs.
- Clean conversational flow with emoji-enhanced replies.

> **Try this:**  
> 🗣️ “Add a schedule at 4PM to study DSA”  
> 🗣️ “Remind me to drink water every 2 hours”  
> 🗣️ “Create a task to finish my ML assignment”

---

### 2. 🦹 Sith Mode Toggle (Chatbot Personality)
- **The Sith toggle transforms the chatbot's behavior and tone — not the UI.**
- Inspired by the Star Wars theme of the hackathon.
- Toggle between:
  - 🧑 **Normal Mode** → Polite, helpful assistant  
  - 🦹 **Sith Mode** → Sarcastic, dark, and cunning like Darth Sidious  
- Makes interaction fun, immersive, and themed around Star Wars.

---

### 3. 📅 Schedule Planner
- Add and manage day-based schedules.
- View today's schedule prominently.
- Automatically stores time-tagged entries for better planning.

---

### 4. ✅ Task Manager
- Create, complete, and delete tasks.
- Tasks are session-persistent.
- Clean UI with Sith-themed visuals.

---

### 5. 📝 Notes Section
- Quick note-taking with titles.
- All notes saved in-session.
- Minimal distraction, focused writing area.

---

### 6. 🎧 Mood-Based Music Player
- Background audio changes based on selected mood:
  - Calm
  - Focus
  - Intense
- Blurred, semi-transparent music widget adds to aesthetic.

> ⚠️ Currently, only a few local songs are available.  
Spotify API integration was not completed in time.

---

### 7. 🧠 Chat History Manager
- Maintain multiple chat sessions.
- Rename, delete, and export past conversations.
- Inline operations (hover menu) for session control.

---

## ✨ Why Star Wars Theme?

This project was built for a **Star Wars-themed hackathon**, so we embraced the dark and powerful aura of the Sith. UI and interactions reflect the mood of:
- 🦹‍♂️ Darth Sidious-like tone in chatbot
- ⚫ Transparent UI with red-accented styling
- 🛰️ Galactic, mysterious vibe throughout

---

## 🚀 Deployment

The app is hosted on **Streamlit Cloud**:  
🔗 [https://sith-studyflow-pmjfrw4iascbgerypsz9y6.streamlit.app/](https://sith-studyflow-pmjfrw4iascbgerypsz9y6.streamlit.app/)

---

## 🔧 Installation & Running Locally

### 1. Clone this repository

```bash
git clone https://github.com/pranavamurthyks/Sith-StudyFlow.git
cd Sith-StudyFlow
```

### 2. Create virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a `.streamlit/secrets.toml` file:

```toml
[api_keys]
groq_api_key = "your_groq_api_key_here"
```

> ⚠️ **Do not commit your secrets.toml** — it's ignored via `.gitignore`.

---

## 📁 File Structure Overview

```
📦 StudyFlow/
 ┣ 📁 .streamlit/
 ┃ ┗ 📄 secrets.toml
 ┣ 📄 app.py                # Main Streamlit app
 ┣ 📄 requirements.txt      # Python dependencies
 ┣ 📄 README.md             # You're reading it!
 ┗ 📁 static/               # Music & assets
```

---

## 📌 Requirements

Here's a sample `requirements.txt`:

```
streamlit
python-dotenv
openai
groq
requests
```

---

## 📍 Domain: AI / ML

This project falls under the **AI/ML domain** because:
- It uses **Groq-hosted LLMs** for natural language interaction.
- Implements **chat memory and tagging** for intelligent assistance.
- Applies mood classification for music selection (UX-level AI).

---

## 💡 Future Improvements

- Spotify API integration with real-time playlist control.
- Voice input/output chatbot (mic + TTS).
- Pomodoro timer linked with schedule/tasks.
- Persistent memory using external DB (e.g., Supabase).
- Improved multi-user support with authentication.
- **User profile creation and customizable preferences.**

---

## ✨ Credits

**Created by:**
- Aravind M  
- Mano Karthik  
- Pranavamurthy K S  
- Raghav Prasanna

---

## 📜 License

MIT License
