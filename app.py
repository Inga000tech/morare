import streamlit as st
import datetime
import json
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Morare", page_icon="🌙", layout="centered")

# --- CUSTOM UI/UX DESIGN (The "Safe Space" CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Lora:ital,wght@0,400;1,400&display=swap');

    /* Background and Container */
    .stApp {
        background-color: #F9F7F2;
    }
    
    .main .block-container {
        max-width: 550px;
        padding-top: 2rem;
    }

    /* Typography */
    h1, h2, h3, p, span, div, textarea {
        font-family: 'Inter', sans-serif;
        color: #2A2A2A;
    }

    .brand-name {
        font-family: 'Lora', serif;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0px;
        font-weight: 400;
    }

    .date-label {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
        color: #9A8C98;
        margin-bottom: 20px;
    }

    /* The Journal Card */
    .journal-card {
        background: white;
        padding: 40px;
        border-radius: 4px;
        border: 1px solid #EAE5D9;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }

    .astro-title {
        font-family: 'Lora', serif;
        font-size: 1.6rem;
        text-align: center;
        margin-bottom: 10px;
    }

    .astro-meaning {
        text-align: center;
        font-weight: 300;
        color: #6B6B6B;
        line-height: 1.6;
        margin-bottom: 30px;
    }

    .prompt-box {
        font-family: 'Lora', serif;
        font-style: italic;
        font-size: 1.25rem;
        text-align: center;
        margin-top: 20px;
        color: #2A2A2A;
        border-top: 1px solid #F0EDE5;
        padding-top: 30px;
    }

    /* Styling the Input Area */
    .stTextArea textarea {
        background-color: transparent !important;
        border: none !important;
        font-family: 'Lora', serif !important;
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
        background-image: linear-gradient(#EEEBDD 1px, transparent 1px) !important;
        background-size: 100% 2.4rem !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- DATA PARSER ---
# This helper reads your existing content.js so you don't have to rewrite it
def load_astro_data():
    with open('content.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the JSON-like object from the JS file using regex
    match = re.search(r'astrologyEvents2026 = (\{.*?\});', content, re.DOTALL)
    if match:
        data_str = match.group(1)
        # Clean up JS keys to make it valid JSON
        data_str = re.sub(r'(\w+):', r'"\1":', data_str)
        return json.loads(data_str)
    return {}

def get_daily_question(day_of_year):
    questions = [
        "What does my 'inner child' need to feel safe today?",
        "What is one noise or distraction I can eliminate this morning?",
        "If I were my own best friend, what encouragement would I give myself right now?",
        "Which 'inner critic' voice is loudest today, and what is its name?",
        "What would 'good enough' look like for today?",
        "What is a 'micro-win' I can celebrate by 10:00 AM?",
        "If today were a movie, what would the genre be?",
        "What is one 'No' I need to say to protect my 'Yes'?",
        "What part of 'Future Me' am I building this morning?",
        "If I had 20% more courage today, what would I do differently?",
        "What is one boundary I need to reinforce today?",
        "What is the 'theme song' for my intentions today?",
        "How can I show up authentically in my first meeting/interaction?",
        "What is one thing I’m doing today purely because I want to?",
        "What legacy—even a tiny one—do I want to leave by tonight?",
        "What am I currently avoiding that needs my attention?",
        "What emotion am I trying to 'fix' rather than feel?",
        "Where am I seeking validation from others today?",
        "What is one 'shadow' trait (like envy or pride) that might pop up today?",
        "How am I subconsciously making things harder for myself?",
        "What is the most honest thing I could say to myself right now?",
        "What am I 'hiding' behind my busyness?",
        "What would happen if I didn't try to be 'perfect' today?",
        "What is the 'unspoken' need behind my current stress?",
        "What is one thing I’m looking forward to in the next 12 hours?",
        "What is a 'tiny luxury' I can grant myself today?",
        "What is something beautiful I saw within five minutes of waking up?",
        "How can I add a moment of 'play' to my afternoon?",
        "What is one thing about my physical space that I appreciate?",
        "What is a strength of mine that I often overlook?",
        "If I were a character in a book, what would the narrator say about me today?",
        "What is one 'soul-nourishing' food or drink I’ll have today?",
        "What is a question I hope someone asks me today?",
        "What is the 'one word' that defines my intention for this day?"
    ]
    return questions[day_of_year % len(questions)]

# --- MAIN APP LOGIC ---
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
day_of_year = today.timetuple().tm_yday

# Header
st.markdown(f'<div class="date-label">{today.strftime("%A, %B %d")}</div>', unsafe_allow_html=True)
st.markdown('<h1 class="brand-name">Morare</h1>', unsafe_allow_html=True)

# Astrology Section
events = load_astro_data()
current_event = events.get(date_str, {
    "title": "Integration Period",
    "meaning": "No major celestial shift today. The work is internal. Integration is where growth becomes permanent."
})

st.markdown(f"""
    <div class="journal-card">
        <div class="astro-title">{current_event['title']}</div>
        <div class="astro-meaning">{current_event['meaning']}</div>
        <div class="prompt-box">{get_daily_question(day_of_year)}</div>
    </div>
""", unsafe_allow_html=True)

# Journal Entry (Web App Feature)
# Using Streamlit session state or local persistent files would go here.
# For simplicity, this uses the built-in text_area.
entry = st.text_area("", placeholder="Spill your thoughts onto the paper...", height=300)

if entry:
    st.info("Your reflection is active for this session. To save permanently in a Streamlit Cloud environment, we would connect a database next!")
