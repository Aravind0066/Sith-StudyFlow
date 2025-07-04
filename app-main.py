# --- Imports ---
import streamlit as st
import pickle
import random
from datetime import datetime, timedelta
import re
import streamlit.components.v1 as components
import requests  
import base64
import time


# --- Streamlit Page Setup ---
st.set_page_config(page_title="StudyFlow - Sith Edition", layout="wide")

# --- Initialize all required session state variables early ---
default_session_state = {
    "selected_tab": "Chatbot",
    "tasks": [],
    "notes": "",
    "schedule_data": [],
    "messages": [],
    "pending_action": None,
    "timeline_log": [],
    "chat_memory": {},  # 🧠 for chat history
    "current_session_id": "Session #1",
    "default_pomo_duration": 25,
    "default_break_duration": 5,
    "pomo_running": False,
    "pomo_end_time": None,
    "pomo_phase": "Focus",  # or "Break"

}

for key, value in default_session_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

PLANET_BACKGROUNDS = {
    "Schedule": "static/planets/dagobah.jpg",
    "Tasks": "static/planets/tatooine.jpg",
    "Notes": "static/planets/hoth.jpg",
    "Pomodoro": "static/planets/coruscant.jpg"
}


# --- Background Image Setup ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

# Convert your image to base64
# Choose different background based on selected tab (except Chatbot)
selected_tab = st.session_state.get("selected_tab", "Chatbot")
if selected_tab == "Chatbot":
    planet_bg_path = "static/bg.jpeg"  # Keep existing Mustafar background
else:
    planet_bg_path = PLANET_BACKGROUNDS.get(selected_tab, "static/bg.jpeg")

img_base64 = get_base64_image(planet_bg_path)


# --- CSS Styling ---
if img_base64:
    # Use f-string to properly inject the base64 image
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Main background container */
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/jpeg;base64,{img_base64}") no-repeat center top fixed !important;
        background-size: cover !important;
        background-position: center 50px !important;
        font-family: 'Press Start 2P', cursive !important;
        color: white !important;
        padding-top: 10px !important;
    }}

    body {{
        background: url("data:image/jpeg;base64,{img_base64}") no-repeat center center fixed !important;
        background-size: cover !important;
        color: #ffcccc;
        font-family: 'Press Start 2P', cursive;
        cursor: url('https://cur.cursors-4u.net/symbols/sym-1/sym93.cur'), auto;
    }}

    @keyframes floater {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
    }}

    .glow {{
        animation: glowPulse 2.5s ease-in-out infinite;
    }}
    
    @keyframes glowPulse {{
        0%, 100% {{ text-shadow: 0 0 5px #ffe81f, 0 0 10px #ffe81f; }}
        50% {{ text-shadow: 0 0 15px #ffe81f, 0 0 25px #ffdd00; }}
    }}

    ::-webkit-scrollbar {{
        width: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: #111;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background-color: #ffe81f;
        border-radius: 10px;
        border: 2px solid #000;
    }}

    /* Dark overlay for better readability */
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: fixed;
        inset: 0;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: -1;
    }}

    /* Make all text use pixel font, scaled accordingly */
    h1, h2, h3, h4, h5, h6, p, div, span, button, input, textarea, label {{
        font-family: 'Press Start 2P', cursive !important;
    }}

    /* Adjust font sizes for better scaling */
    h1 {{ font-size: 1.8rem; }}
    h2 {{ font-size: 1.5rem; }}
    h3 {{ font-size: 1.3rem; }}
    p, label, div, span, button, input, textarea {{ font-size: 0.85rem; }}

    /* Header container */
    .main-header {{
        position: relative;
        top: 10px;
        left: 30px;
        max-width: 90%;
    }}

    /* Main Title */
    .main-title {{
        font-size: 2.2rem;
        color: #ffe81f;
        line-height: 2.8rem;
        text-shadow: 1px 1px 0 #000;
    }}

    /* Quote */
    .subtext {{
        display: block;
        font-size: 0.6rem;
        margin-top: 0.6rem;
        color: #ffe81f;
        font-style: italic;
        text-shadow: 1px 1px 0 #000;
    }}

    /* Chat container styling */
    [data-testid="stChatInputContainer"] {{
        background-color: transparent !important;
        padding: 0 !important;
        margin-top: 20px;
    }}

    /* Chat input styling - BIGGER TEXT AREA */
    section[data-testid="stChatInput"] {{
        position: relative !important;
        width: 100% !important;
        background-color: transparent !important;
        padding: 0 !important;
        margin-top: 20px;
    }}

    section[data-testid="stChatInput"] textarea {{
        width: 100% !important;
        min-height: 200px !important;
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: #ffe81f !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 14px !important;
        border: 4px solid #ffe81f !important;
        border-radius: 0px !important;
        padding: 20px !important;
        box-shadow: inset 0 0 0 2px black;
        margin-top: 0 !important;
        resize: vertical !important;
    }}

    section[data-testid="stChatInput"] textarea:focus {{
        outline: none !important;
        box-shadow: inset 0 0 0 2px #000000;
    }}

    /* Chat message container */
    [data-testid="chatMessage"] {{
        background-color: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #ffe81f !important;
        border-radius: 0 !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
    }}

    /* Remove extra padding around chat */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] {{
        gap: 0 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
else:
    # Fallback CSS without background image
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

    /* Fallback background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        font-family: 'Press Start 2P', cursive !important;
        color: white !important;
        padding-top: 60px !important;
    }

    body {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        color: #ffcccc;
        font-family: 'Press Start 2P', cursive;
    }

    /* Rest of your styles remain the same */
    h1, h2, h3, h4, h5, h6, p, div, span, button, input, textarea, label {
        font-family: 'Press Start 2P', cursive !important;
    }

    h1 { font-size: 1.8rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.3rem; }
    p, label, div, span, button, input, textarea { font-size: 0.85rem; }
    </style>
    """, unsafe_allow_html=True)
    st.warning("⚠ Background image not found. Using fallback styling.")

# --- Streamlit Config & Styling ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Orbitron&display=swap" rel="stylesheet">
<style>
body { font-family: 'Orbitron', sans-serif; background-color: #0a0a0a; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1a1a1a, #000000); }
[data-testid="stSidebar"] .stButton>button {
    width: 100%; height: 54px; font-size: 20px;
    background: #111 !important; border: none; border-radius: 14px;
    color: #fff; cursor: pointer;
    box-shadow: 0 5px 0 #ff1a1a;
    transition: transform .25s cubic-bezier(.34,1.56,.64,1), box-shadow .25s;
    animation: floater 5s ease-in-out infinite;
}
[data-testid="stSidebar"] .stButton>button:hover {
    animation-play-state: paused;
    transform: scale(1.3) translateY(-3px);
    box-shadow: 0 15px 20px rgba(255, 0, 0, .75);
}
[data-testid="stSidebar"] .stButton>button:active {
    transform: scale(1.15) translateY(1px);
    box-shadow: 0 4px 8px rgba(255, 0, 0, .75);
}
@keyframes floater {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-4px); }
}
.music-player { background-color: #111; border-radius: 12px; box-shadow: 0 0 10px #ff1a1a88; padding: 10px; margin-bottom: 10px; }
.main-header { text-align: center; padding: 2rem; background: rgba(255, 0, 0, 0.05); border-radius: 15px; margin-bottom: 1rem; color: #ff4d4d; }
</style>
""", unsafe_allow_html=True)


# --------------------  Random Sith Quote  ----------------------
SITH_QUOTES = [
    "Good… Good. Let the hate flow through you.",
    "I am the Senate.",
    "Did you ever hear the tragedy of Darth Plagueis the Wise?",
    "Your feeble skills are no match for the power of the Dark Side.",
    "Everything that has transpired has done so according to my design."
]
# --- Sith Quote Logic with 30s timer ---
if "sith_quote" not in st.session_state:
    st.session_state.sith_quote = random.choice(SITH_QUOTES)
    st.session_state.quote_last_updated = time.time()
else:
    now = time.time()
    if now - st.session_state.quote_last_updated > 10:  # 30 seconds
        st.session_state.sith_quote = random.choice(SITH_QUOTES)
        st.session_state.quote_last_updated = now

st.sidebar.markdown(f"🗨 {st.session_state.sith_quote}")



# --- Sidebar Options ---
st.sidebar.markdown("## 🧠 Personality")
sith_mode = st.sidebar.toggle("🌑 Enable Sith Mode", value=True)

# --- Chat History Dropdown with Inline Rename ---
st.sidebar.markdown("## 💾 Chat History")

session_keys = list(st.session_state.chat_memory.keys())
if st.session_state.current_session_id not in session_keys:
    session_keys.append(st.session_state.current_session_id)

selected_session = st.sidebar.selectbox("📂 Select Session", session_keys, index=session_keys.index(st.session_state.current_session_id))

if selected_session != st.session_state.current_session_id:
    st.session_state.current_session_id = selected_session
    st.session_state.messages = st.session_state.chat_memory[selected_session].copy()
    st.rerun()



# --- Navigation Buttons ---
st.sidebar.markdown("## 🧱 Navigate the Empire")
icon_map = {
    "Chatbot": "👑",
    "Schedule": "🌌",
    "Tasks": "⚔",
    "Notes": "📖",
    "Pomodoro": "🚀"
}

for section, emoji in icon_map.items():
    if st.sidebar.button(f"{emoji} {section}", key=f"nav_{section}"):
        st.session_state.selected_tab = section
        st.rerun()




# --- Banner ---
st.markdown("""
<div class="main-header">
    <h1 class="glow">
    ⚡ <span class="main-title">STUDY FLOW: SITH LORD EDITION</span>
        <span class="subtext">"Power! Unlimited power!" – Your path to dark side productivity</span>
    </h1>
</div>
""", unsafe_allow_html=True)

# --- Chat Reset Button ---
if st.session_state.selected_tab == "Chatbot":
    col1, col2, col3 = st.columns([5, 1, 2])

    # 🧹 New Chat Button
    with col2:
        if st.button("🧹 New Chat"):
            # Save current chat to memory
            if st.session_state.messages:
                st.session_state.chat_memory[st.session_state.current_session_id] = st.session_state.messages

            # Create new session ID
            new_session_id = datetime.now().strftime("Chat %Y-%m-%d %H:%M:%S")
            st.session_state.current_session_id = new_session_id
            st.session_state.messages = []
            st.session_state.chat_memory[new_session_id] = st.session_state.messages
            st.session_state.timeline_log.append({
                "time": datetime.now().strftime("%H:%M"),
                "event": f"Started new chat session: {new_session_id}"
            })
            st.rerun()

    # ✏ Rename / 🗑 Delete / 📤 Export Expander
    with col3:
        with st.expander("✏ Rename / Manage"):
            new_name = st.text_input("Rename to:", key="inline_rename_input")

            if st.button("✅ Apply Rename"):
                old_id = st.session_state.current_session_id
                chat_memory = st.session_state.chat_memory

                if old_id not in chat_memory:
                    st.warning("⚠ Session not found in memory. Cannot rename.")
                elif not new_name or new_name in chat_memory:
                    st.warning("⚠ Name is empty or already exists.")
                else:
                    chat_memory[new_name] = chat_memory.pop(old_id)
                    st.session_state.current_session_id = new_name
                    st.session_state.messages = chat_memory[new_name]
                    st.success(f"Session renamed to {new_name}!")
                    st.rerun()

            # 🗑 Delete Button
            if st.button("🗑 Delete Chat"):
                del_id = st.session_state.current_session_id
                if del_id in st.session_state.chat_memory:
                    st.session_state.chat_memory.pop(del_id)
                    st.session_state.timeline_log.append({
                        "time": datetime.now().strftime("%H:%M"),
                        "event": f"Deleted chat session: {del_id}"
                    })

                    # Load fallback or reset
                    if st.session_state.chat_memory:
                        fallback_id = list(st.session_state.chat_memory.keys())[-1]
                        st.session_state.current_session_id = fallback_id
                        st.session_state.messages = st.session_state.chat_memory[fallback_id]
                    else:
                        st.session_state.current_session_id = "Session #1"
                        st.session_state.messages = []
                        st.session_state.chat_memory = {}

                    st.success(f"Deleted session: {del_id}")
                    st.rerun()
                else:
                    st.warning("⚠ No such session found to delete.")

            # 📤 Export Button
            if st.button("📤 Export Chat"):
                session_id = st.session_state.current_session_id
                chat = st.session_state.chat_memory.get(session_id, [])
                if chat:
                    export_text = "\n\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat])
                    st.download_button(
                        label="⬇ Download Chat Log",
                        data=export_text,
                        file_name=f"{session_id.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )
                else:
                    st.info("No messages to export.")
  



# --- Load chatbot model using Groq API ---
def get_bot_response(prompt, sith_mode=False):
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['groq_token']}",
        "Content-Type": "application/json"
    }
    system_prompt = (
        "You are a Sith Lord AI assistant. Speak with flair, use phrases like 'young apprentice', and channel the dark side. "
        "If the user is giving a command related to adding a task, schedule, or note, end your response with one of the tags: [task_add], [schedule_add], or [notes_update]. "
        "Do NOT explain the tag. Simply put the tag at the end of your response."
        if sith_mode else
        "You are a helpful and intelligent study assistant. Respond clearly and politely in simple English. "
        "If the user gives an instruction related to tasks, schedules, or notes, end your reply with a tag: [task_add], [schedule_add], or [notes_update]. "
        "Only include the tag at the end of your response. No explanation is needed."
    )
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        tag = detect_action_tag(reply)
        if tag:
            reply = reply.replace(f"[{tag}]", "").strip()
        return reply, tag
    else:
        return f"❌ API error {response.status_code}: {response.text}", None




# --- Helper Functions ---
def analyze_notes(notes):
    if "math" in notes.lower(): return "Review formulas and do practice problems."
    if "history" in notes.lower(): return "Create a timeline of events."
    if "code" in notes.lower(): return "Build mini projects and practice logic."
    return "Summarize in your own words using the Feynman method."

def detect_action_tag(text):
    text = text.lower()
    for t in ["task_add", "schedule_add", "notes_update"]:
        if f"[{t}]" in text:
            return t
    return None


def extract_time_and_task(text):
    # Example: "Tomorrow at 3pm study DSA" → ("15:00", "study DSA")
    time_match = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b", text.lower())
    task = re.sub(r"\b(at|on)?\s*\d{1,2}(:\d{2})?\s*(am|pm)?", "", text, flags=re.IGNORECASE).strip()
    
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        period = time_match.group(3)

        if period == "pm" and hour != 12:
            hour += 12
        elif period == "am" and hour == 12:
            hour = 0
        time_str = f"{hour:02d}:{minute:02d}"
    else:
        time_str = "00:00"

    return time_str, task or "Untitled Task"

def get_ai_priority(task_text):
    keywords = {"urgent": "High", "soon": "Medium", "later": "Low"}
    for word, priority in keywords.items():
        if word in task_text.lower():
            return priority
    return random.choice(["High", "Medium", "Low"])

def detect_mood_from_chat():
    recent_text = " ".join([m["content"] for m in st.session_state.messages[-5:]]).lower()
    if any(word in recent_text for word in ["tired", "bored", "lazy", "stress"]):
        return "Stressed"
    elif any(word in recent_text for word in ["excited", "start", "ready"]):
        return "Energetic"
    elif any(word in recent_text for word in ["focus", "study", "work"]):
        return "Focused"
    elif any(word in recent_text for word in ["idea", "design", "project"]):
        return "Creative"
    else:
        return "Relaxed"



# Music Player

if st.toggle("🎵 Music Player", key="mood_toggle"):

    # Dropdown to select mood
    selected_mood = st.selectbox(
        "🎧 Select your current mood:",
        ["Focused", "Relaxed", "Energetic", "Stressed", "Creative"],
        index=0,
        key="selected_mood_dropdown"
    )

    # Map moods to URLs (replace with your actual music URLs)
    mood_to_url = {
        "Focused": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "Relaxed": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "Energetic": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "Stressed": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "Creative": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    }

    # Get the audio URL for selected mood
    audio_url = mood_to_url[selected_mood]

    # Display music player
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
    
    /* Hide the default keyboard arrow icon */
    .stSelectbox > div > div > div > div:first-child {{
        display: none !important;
    }}
    
    /* Hide default toggle icons */
    .stCheckbox > label > div:first-child {{
        display: none !important;
    }}
    
    /* Custom toggle styling */
    .stCheckbox > label {{
        background: linear-gradient(135deg, #1f1f1f, #0d0d0d);
        border: 2px solid #ffe81f;
        border-radius: 10px;
        padding: 10px 15px;
        color: #ffe81f;
        font-family: 'Press Start 2P', cursive;
        font-size: 12px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .stCheckbox > label:hover {{
        box-shadow: 0 0 15px #ffe81f88;
        transform: translateY(-2px);
    }}
    
    .stCheckbox > label:before {{
        content: "🎵";
        font-size: 16px;
        margin-right: 5px;
    }}
    
    /* Custom selectbox styling */
    .stSelectbox > div > div {{
        background: linear-gradient(135deg, #1f1f1f, #0d0d0d) !important;
        border: 2px solid #ffe81f !important;
        border-radius: 10px !important;
        color: #ffe81f !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 12px !important;
    }}
    
    .stSelectbox > div > div:before {{
        content: "🎧 ";
        font-size: 14px;
        margin-right: 8px;
    }}
    
    .modern-player {{
        background: linear-gradient(135deg, #1f1f1f, #0d0d0d);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 0 10px #ff4d4d99;
        color: white;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        font-family: 'Orbitron', sans-serif;
        margin-bottom: 10px;
        border: 2px solid #ffe81f;
    }}
    .song-info {{ 
        flex: 2; 
        display: flex;
        flex-direction: column;
        gap: 5px;
    }}
    .song-title {{ 
        font-size: 18px; 
        font-weight: bold; 
        color: #ffe81f;
    }}
    .song-mood {{ 
        font-size: 14px; 
        color: #ff4d4d; 
        margin-top: 4px; 
    }}
    .audio-box {{ 
        flex: 3; 
    }}
    .custom-audio {{
        width: 100%;
        height: 40px;
        border-radius: 10px;
        outline: none;
        background: #000;
        border: 2px solid #ffe81f;
    }}
    .custom-audio::-webkit-media-controls-panel {{
        background-color: #000;
        border: 2px solid #ffe81f;
    }}
    </style>

    <div class="modern-player">
        <div class="song-info">
            <div class="song-title">⚡ Study Flow Radio</div>
            <div class="song-mood">{selected_mood} Mode Activated</div>
        </div>
        <div class="audio-box">
            <audio controls autoplay class="custom-audio" key="{selected_mood}">
                <source src="{audio_url}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        </div>
    </div>

    <script>
    // Force audio reload when mood changes
    document.addEventListener('DOMContentLoaded', function() {{
        const audio = document.querySelector('audio');
        if (audio) {{
            audio.load();
            audio.play();
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

    # Force audio reload using JavaScript (backup)
    st.markdown(f"""
    <script>
    setTimeout(function() {{
        const audio = document.querySelector('audio.custom-audio');
        if (audio) {{
            audio.src = '{audio_url}';
            audio.load();
            audio.play().catch(e => console.log('Auto-play blocked by browser'));
        }}
    }}, 100);
    </script>
    """, unsafe_allow_html=True)







# --- TABS LOGIC ---

if st.session_state.selected_tab == "Chatbot":

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            role_icon = "🧑"
            role_name = "Apprentice" if sith_mode else "You"
        else:
            role_icon = "🤖"
            role_name = "Darth Sidious" if sith_mode else "StudyBot"

        with st.chat_message(msg["role"]):
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.7);border:2px solid #ffe81f;
                    padding:10px;margin-bottom:10px;border-radius:0;
                    box-shadow:0 0 8px #ffe81f88;font-size:0.9rem;'>
            {role_icon} <b>{role_name}:</b><br>{msg["content"]}
        </div>
        """, unsafe_allow_html=True)


    # Chat input
    placeholder_text = (
        "What’s on your mind, apprentice?" if sith_mode
        else "Need help planning your day?"
    )
    prompt = st.chat_input(placeholder_text)

    if prompt:
        # Append user's message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get AI response and tag
        response, tag = get_bot_response(prompt, sith_mode=sith_mode)
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 🔄 Step 4: Save current messages into chat memory under session ID
        st.session_state.chat_memory[st.session_state.current_session_id] = st.session_state.messages.copy()

        # Task handling
        if tag == "task_add":
            st.session_state.tasks.append({
                'task': prompt,
                'completed': False,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'priority': get_ai_priority(prompt)
            })
            st.session_state.messages.append({"role": "assistant", "content": "📝 Task added to your list."})
            st.session_state.timeline_log.append({
                "time": datetime.now().strftime("%H:%M"),
                "event": f"Task added: {prompt}"
            })

        # Schedule handling
        elif tag == "schedule_add":
            time_str, task = extract_time_and_task(prompt)
            st.session_state.schedule_data.append({'day': "Today", 'time': time_str, 'task': task})
            st.session_state.messages.append({"role": "assistant", "content": f"📅 Schedule created: {task} at {time_str}"})
            st.session_state.timeline_log.append({
                "time": datetime.now().strftime("%H:%M"),
                "event": f"Scheduled: {task} at {time_str}"
            })

        # Notes handling
        elif tag == "notes_update":
            st.session_state.notes += f"\n- {prompt}"
            st.session_state.messages.append({"role": "assistant", "content": "🧠 Noted in your Smart Notes."})
            st.session_state.timeline_log.append({
                "time": datetime.now().strftime("%H:%M"),
                "event": "Note updated from chat"
            })

        st.rerun()


elif st.session_state.selected_tab == "Schedule":
    st.subheader("🌌 Galactic Schedule")

    day = st.selectbox("Select day", ["Today", "Tomorrow", "Custom"])
    time = st.time_input("Select time")
    task = st.text_input("What will you do at that time?")

    if st.button("Add to Schedule"):
        st.session_state.schedule_data.append({'day': day, 'time': str(time), 'task': task})
        st.success("Added to schedule!")

    if st.session_state.schedule_data:
        st.markdown("### Your Schedule")
        for item in st.session_state.schedule_data:
            st.markdown(f"- 🕒 {item['time']} ({item['day']}): {item['task']}")

elif st.session_state.selected_tab == "Tasks":
    st.subheader("⚔ Mission Orders")

    # --- Task Input ---
    with st.form("add_task_form", clear_on_submit=True):
        new_task = st.text_input("Add a new task:")
        submitted = st.form_submit_button("Add Task")

        if submitted and new_task:
            priority = get_ai_priority(new_task)
            st.session_state.tasks.append({
                'task': new_task,
                'completed': False,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'priority': priority
            })
            st.success(f"Added with {priority} priority!")
            st.rerun()

    # --- Task Stats ---
    total_tasks = len(st.session_state.tasks)
    completed_count = sum(task['completed'] for task in st.session_state.tasks)

    if total_tasks > 0:
        progress = completed_count / total_tasks
        progress_percent = int(progress * 100)

        st.markdown(f"""
        <style>
        .lightsaber-bar {{
            background-color: #222;
            border: 2px solid #ff1a1a;
            border-radius: 8px;
            height: 25px;
            width: 100%;
            margin-top: 10px;
            box-shadow: 0 0 8px #ff1a1a66;
            overflow: hidden;
        }}
        .lightsaber-fill {{
            height: 100%;
            width: {progress_percent}%;
            background: linear-gradient(90deg, #ff1a1a, #ff6666);
            box-shadow: 0 0 15px #ff1a1a;
            transition: width 0.4s ease-in-out;
        }}
        </style>
        <div class="lightsaber-bar">
            <div class="lightsaber-fill"></div>
        </div>
        <p style='text-align:center; color:#ffe81f; font-family:monospace;'>Lightsaber Charging: {completed_count}/{total_tasks} Tasks Completed</p>
        """, unsafe_allow_html=True)

    # --- Task List Display ---
    for i in range(len(st.session_state.tasks)):
        task = st.session_state.tasks[i]
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            emoji = "🔴" if task['priority'] == "High" else "🟡" if task['priority'] == "Medium" else "🟢"
            st.markdown(f"{emoji} {task['task']}")
        with col2:
            new_val = st.checkbox("Done", key=f"done_{i}", value=task['completed'])
            if new_val != task['completed']:
                st.session_state.tasks[i]['completed'] = new_val
                st.rerun()
        with col3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()




elif st.session_state.selected_tab == "Notes":
    st.subheader("📝 Holocron Logs")

    st.session_state.notes = st.text_area("Write your notes here...", value=st.session_state.notes, height=300)

    if st.session_state.notes:
        if st.button("🧠 Analyze Notes"):
            suggestion = analyze_notes(st.session_state.notes)
            st.markdown(f"💡 Suggestion:** {suggestion}")


# Initialize session state variables
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Pomodoro"

if "pomo_phase" not in st.session_state:
    st.session_state.pomo_phase = "Focus"

if "pomo_running" not in st.session_state:
    st.session_state.pomo_running = False

if "pomo_end_time" not in st.session_state:
    st.session_state.pomo_end_time = None

if "default_pomo_duration" not in st.session_state:
    st.session_state.default_pomo_duration = 25

if "default_break_duration" not in st.session_state:
    st.session_state.default_break_duration = 5

# --- POMODORO TAB ---
from datetime import datetime, timedelta
import streamlit as st
import time

if st.session_state.selected_tab == "Pomodoro":
    st.subheader("🚀 Sith Pomodoro Mode")

    # Timer input
    col1, col2 = st.columns(2)
    with col1:
        focus_minutes = st.number_input("Focus Time (min)", value=st.session_state.default_pomo_duration)
    with col2:
        break_minutes = st.number_input("Break Time (min)", value=st.session_state.default_break_duration)

    # Rocket animation placeholder
    rocket_placeholder = st.empty()

    # Show rocket animation only during focus phase while running
    if st.session_state.pomo_running and st.session_state.pomo_phase == "Focus":
        rocket_placeholder.markdown("""
        <style>
        @keyframes zigzag-fly {
            0%   { transform: translate(0vw, 0px) rotate(-10deg); }
            20%  { transform: translate(20vw, -30px) rotate(5deg); }
            40%  { transform: translate(40vw, 30px) rotate(-5deg); }
            60%  { transform: translate(60vw, -20px) rotate(8deg); }
            80%  { transform: translate(80vw, 20px) rotate(-8deg); }
            100% { transform: translate(100vw, 0px) rotate(0deg); }
        }

        .zigzag-rocket {
            font-size: 60px;
            position: absolute;
            top: 20px;
            left: 0;
            z-index: 999;
            animation: zigzag-fly 12s linear infinite;
        }

        .rocket-wrapper {
            position: relative;
            height: 150px;
            overflow: hidden;
        }
        </style>
        <div class="rocket-wrapper">
            <span class="zigzag-rocket">🚀</span>
        </div>
        """, unsafe_allow_html=True)

    # Start button
    if not st.session_state.pomo_running:
        if st.button("▶ Start Timer"):
            st.session_state.pomo_running = True
            st.session_state.pomo_phase = "Focus"
            st.session_state.pomo_end_time = datetime.now() + timedelta(minutes=focus_minutes)
            st.rerun()

    # Timer logic
    if st.session_state.pomo_running:
        now = datetime.now()
        remaining = st.session_state.pomo_end_time - now

        if remaining.total_seconds() <= 0:
            if st.session_state.pomo_phase == "Focus":
                st.session_state.pomo_phase = "Break"
                st.session_state.pomo_end_time = datetime.now() + timedelta(minutes=break_minutes)
            else:
                st.session_state.pomo_phase = "Focus"
                st.session_state.pomo_end_time = datetime.now() + timedelta(minutes=focus_minutes)
            st.rerun()

        mins, secs = divmod(int(remaining.total_seconds()), 60)
        st.markdown(
            f"<h2 style='text-align:center; color:#ffe81f;'>⏳ {st.session_state.pomo_phase} Time: {mins:02d}:{secs:02d}</h2>",
            unsafe_allow_html=True
        )
        time.sleep(1)
        st.rerun()
