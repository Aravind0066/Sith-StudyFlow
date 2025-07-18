# 🧠 Sith StudyFlow - AI-Powered Productivity Companion

Welcome to **Sith StudyFlow**, a Streamlit-powered productivity dashboard infused with the power of **Groq AI** and **Darth Sidious-inspired UI**. Whether you're planning your tasks, chatting with your AI assistant, or listening to mood-based music, this tool brings AI and organization into perfect harmony.

---

## 🏆 About the Hackathon

This project was built for **Prompt Wars**, a Star Wars-themed hackathon conducted by the **Android Club of VIT Chennai**, which saw participation from over **190 teams** across various domains.

We're proud to say that we secured **🥈 2nd place** in this highly competitive event!

### 🤖 Prompt-Centric Development

In line with the hackathon's core theme of "Prompt Wars," we designed and implemented this project using **AI-assisted development with ChatGPT**.

While the **ideas, logic, and user experience design were fully conceptualized by our team**, the majority of the **coding was accelerated through GPT-powered prompting** — showcasing how developers can now collaborate with AI to build working prototypes quickly and creatively.

This approach reflects real-world trends where **prompt engineering and AI co-development** are becoming key productivity tools in software engineering.

---

## 🧩 Problem Statement

As students, we often juggle multiple tools:

- 🎧 **Spotify** for music  
- 📝 **Notion/Excel** for schedules and task tracking  
- 🤖 **ChatGPT** for questions and productivity help

Constantly switching between them felt fragmented and inefficient. So, we decided to combine all three into one unified platform:

> 🎶 Mood-based music + 🗓 Productivity planner + 🤖 AI assistant

This is a **basic prototype** built during a **Star Wars-themed hackathon** and has **massive potential for future scaling**.

📽 Want to see our pitch visually?  
👉 [Gamma Deck: Study Flow – AI-Powered Productivity Companion](https://gamma.app/docs/Study-Flow-AI-Powered-Productivity-Companion-w1vmfoozw4jd8pq)

> ⚠ **Note:**  
> - Only limited local music tracks are available right now.  
> - Spotify API was attempted but couldn't be integrated in time.  
> - The chatbot's mood-based history could eventually be used to **trigger dynamic playlist changes on Spotify** based on how the user feels — an idea for future development!

---

## 🌟 Features

### 1. 🤖 AI Chatbot (Groq API Powered)
- Chat with a large language model using **Groq's ultra-fast API**.
- Built-in **memory support**: the bot remembers your past queries.
- Session manager with options to **rename, delete, and export chats**.
- Natural conversational tone with emojis, context understanding, and productivity intent tagging.

> **Try this:**  
> 🗣 "Add a schedule at 4PM to study DSA"  
> 🗣 "Remind me to drink water every 2 hours"  
> 🗣 "Create a task to finish my ML assignment"

---

### 2. 🦹 Sith Mode Toggle (Chatbot Personality, Not UI)

Located on the **left sidebar**, this is one of the most **unique and immersive** features.

> ⚠ This **does NOT change the UI** — it alters the **AI chatbot's behavior and tone**.

- In **Normal Mode**, the bot is friendly, supportive, and helpful.
- In **Sith Mode**, the chatbot becomes a **dark, sarcastic, Darth Sidious-like assistant**.
- All responses are themed around **Sith ideology**, sarcasm, and power.

#### 🧪 Example:

| Mode          | Response                                                                 |
|---------------|--------------------------------------------------------------------------|
| Normal Mode   | "Sure! I've scheduled your DSA session at 4PM. Don't forget to take breaks!" |
| Sith Mode     | "Excellent… your fate to study DSA at 4PM is now sealed. The dark side approves." |

> 🦹 Flip the toggle and experience the dark side through AI.

---

### 3. 📅 Schedule Planner
- Add schedules with time-based entries.
- Auto-sorted by time.
- Today's tasks appear prominently.

---

### 4. ✅ Task Manager
- Add tasks, mark them complete, or delete them.
- Tasks persist across sessions.
- Simple UI built for flow-state productivity.

---

### 5. 📝 Notes Section
- Add short notes with languages.
- Meant for study tips, reminders, or scratchpad use.

---

### 6. 🎧 Mood-Based Music Player
- Select mood (Calm, Focus, Intense) to change music vibe.
- Background music auto-updates based on mood.
- Semi-transparent, blurred audio widget for clean UX.

> 💡 Currently uses a **local playlist** due to time limits.  
> Planned: dynamic Spotify playlist switching based on chatbot emotion.

> 👀 **Don't miss the tiny 3D rocket animation in Pomodoro timer!** 🚀

---

### 7. 🧠 Chat History Manager
- View all previous chat sessions.
- Rename chats, delete old ones, and export to .txt.
- Hover-based controls for minimal clutter.

---

## ✨ Why Star Wars Theme?

This project was built for a **Star Wars-themed hackathon**. We embraced the **dark aesthetic and philosophical contrast** between Sith and Jedi:

- Darth Sidious-style chatbot tone  
- Transparent black/red UI  
- Sith mode with sarcastic, dominating AI tone  
- Galactic vibes via music, visuals, and layout  

---

## 🚀 Deployment

Hosted on **Streamlit Cloud**:  
🔗 [Try Sith StudyFlow now](https://sith-studyflow-pmjfrw4iascbgerypsz9y6.streamlit.app/)

📽 Want to see our idea pitch visually?  
👉 [Gamma Presentation](https://gamma.app/docs/Study-Flow-AI-Powered-Productivity-Companion-w1vmfoozw4jd8pq)

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

Create a .streamlit/secrets.toml file:

```toml
[api_keys]
groq_api_key = "your_groq_api_key_here"
```

> ⚠ Do **not** commit your API key or secrets.toml. It's safely excluded via .gitignore.

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

Here's a sample requirements.txt:

```
streamlit
python-dotenv
openai
groq
requests
```

---

## 📍 Domain: AI / ML

This project falls under **AI/ML** because:

- It uses a **Groq-hosted LLM** for natural conversation.  
- Applies **chat memory, context understanding, and mood-based UI logic**.  
- Future extensions include **emotion detection** and **Spotify control via AI mood**.

---

## 💡 Future Improvements

- Spotify API integration (dynamic mood-based playlists)  
- Voice input/output assistant (microphone + TTS)  
- Persistent memory via Supabase or Firebase  
- Pomodoro timer integration with tasks  
- Multi-user authentication support  
- **User profile creation & customization**

---

## ✨ Created By

- [Aravind M](https://github.com/Aravind0066)  
- [Mano Karthik](https://github.com/mano45-sudo)  
- [Pranavamurthy K S](https://github.com/pranavamurthyks)  
- [Raghav Prasanna](https://github.com/RaghavPrasanna9207)

---

## 📜 License

MIT License
