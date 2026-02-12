import streamlit as st
import datetime
import json
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Morare", page_icon="🌙", layout="centered")

# --- DATA PARSING ENGINE ---
def load_js_data():
    """Expert-level regex parser to read JS objects from content.js as Python Dicts/Lists"""
    try:
        with open('content.js', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Parse Astrology Events
        astro_match = re.search(r'astrologyEvents2026 = (\{.*?\});', content, re.DOTALL)
        astro_data = {}
        if astro_match:
            data_str = astro_match.group(1)
            # Make JS keys JSON compatible (wrap keys in quotes)
            data_str = re.sub(r'(\s)(\w+):', r'\1"\2":', data_str)
            # Remove trailing commas that break JSON
            data_str = re.sub(r',\s*\}', '}', data_str)
            astro_data = json.loads(data_str)

        # 2. Parse Lists (Questions, History, Quotes)
        def get_list(var_name):
            match = re.search(rf'{var_name} = \[(.*?)\];', content, re.DOTALL)
            if match:
                items = re.findall(r'"(.*?)"', match.group(1))
                return items
            return []

        return {
            "events": astro_data,
            "questions": get_list("dailyQuestions"),
            "history": get_list("historicalInspirations"),
            "quotes": get_list("poeticQuotes")
        }
    except Exception as e:
        st.error(f"Error loading content.js: {e}")
        return {"events": {}, "questions": [], "history": [], "quotes": []}

# --- STYLING (The Journal UI/UX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

    /* Global Body */
    .stApp {
        background-color: #F9F7F2; /* Warm paper color */
    }

    .main .block-container {
        max-width: 600px;
        padding-top: 3rem;
    }

    /* Branding */
    .brand-name {
        font-family: 'Lora', serif;
        font-size: 3.2rem;
        text-align: center;
        color: #2A2A2A;
        margin-bottom: 0px;
    }

    .date-header {
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-size: 0.8rem;
        color: #9A8C98;
        margin-bottom: 40px;
    }

    /* Word of the Day Mantra */
    .word-label {
        text-align: center;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 4px;
        color: #9A8C98;
        margin-bottom: 5px;
    }
    .word-text {
        font-family: 'Lora', serif;
        font-size: 2.2rem;
        text-align: center;
        color: #4A4A4A;
        margin-bottom: 30px;
    }

    /* The Astrology Card */
    .astro-card {
        background: white;
        padding: 35px;
        border-radius: 2px;
        border: 1px solid #EAE5D9;
        box-shadow: 0 10px 40px rgba(0,0,0,0.04);
        margin-bottom: 30px;
    }

    .astro-title {
        font-family: 'Lora', serif;
        font-size: 1.5rem;
        color: #2A2A2A;
        margin-bottom: 12px;
        border-bottom: 1px solid #F9F7F2;
        padding-bottom: 10px;
    }

    .astro-meaning {
        font-weight: 300;
        color: #6B6B6B;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 25px;
    }

    /* History & Prompt UI */
    .history-box {
        background: #FDFBFA;
        padding: 20px;
        border-radius: 4px;
        border-left: 2px solid #9A8C98;
        font-size: 0.9rem;
        color: #5A5A5A;
        margin-bottom: 25px;
    }

    .prompt-text {
        font-family: 'Lora', serif;
        font-style: italic;
        font-size: 1.2rem;
        color: #2A2A2A;
        text-align: center;
        padding: 10px 0;
    }

    /* THE LINED PAPER TEXT AREA */
    div[data-baseweb="textarea"] {
        background-color: white !important;
        border: 1px solid #EAE5D9 !important;
        border-radius: 0px !important;
        padding: 10px !important;
        /* Red Margin Line */
        background-image: 
            linear-gradient(to right, transparent 39px, #FADADD 40px, transparent 41px),
            linear-gradient(#EEEBDD 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 2.5rem !important; /* Lines every 2.5rem */
    }

    textarea {
        background: transparent !important;
        font-family: 'Lora', serif !important;
        font-size: 1.15rem !important;
        line-height: 2.5rem !important; /* Must match the background-size above */
        padding-left: 50px !important; /* Space for the red margin */
        color: #3E3E3E !important;
    }

    /* Poetic Quote */
    .quote-footer {
        font-family: 'Lora', serif;
        font-style: italic;
        text-align: center;
        padding: 40px 20px;
        color: #9A8C98;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
data = load_js_data()
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")
day_index = today.timetuple().tm_yday # Used for rotating content

# 1. Header & Date
st.markdown(f'<div class="date-header">{today.strftime("%A, %B %d")}</div>', unsafe_allow_html=True)
st.markdown('<h1 class="brand-name">Morare</h1>', unsafe_allow_html=True)

# 2. Determine Event and Word
event = data['events'].get(date_str)
if not event:
    # Integration Day Logic
    grounding_words = ["Balance", "Presence", "Grounding", "Peace", "Stillness", "Breath"]
    word = grounding_words[day_index % len(grounding_words)]
    title = "Integration Period"
    meaning = "No major celestial shift today. The work is internal. Integration is where growth becomes permanent."
else:
    word = event.get('word', 'Presence')
    title = event['title']
    meaning = event['meaning']

# 3. Render Mantra & Astrology Card
st.markdown(f'<div class="word-label">Mantra of the Day</div>', unsafe_allow_html=True)
st.markdown(f'<div class="word-text">{word}</div>', unsafe_allow_html=True)

# Select rotating content
current_history = data['history'][day_index % len(data['history'])] if data['history'] else "No history today."
current_prompt = data['questions'][day_index % len(data['questions'])] if data['questions'] else "What is on your heart?"
current_quote = data['quotes'][day_index % len(data['quotes'])] if data['quotes'] else "Live your truth."

st.markdown(f"""
    <div class="astro-card">
        <div class="astro-title">{title}</div>
        <div class="astro-meaning">{meaning}</div>
        <div class="history-box">
            <strong>Historical Resilience:</strong><br>{current_history}
        </div>
        <div class="prompt-text">“{current_prompt}”</div>
    </div>
""", unsafe_allow_html=True)

# 4. Journal Paper (Input)
user_entry = st.text_area("Journal Entry", height=400, label_visibility="collapsed", placeholder="Let the ink flow...")

# 5. Footer Quote
st.markdown(f'<div class="quote-footer">{current_quote}</div>', unsafe_allow_html=True)

# --- SAVE FEATURE (Optional Mockup) ---
if user_entry:
    st.download_button(
        label="Download Today's Entry",
        data=f"Morare Entry - {date_str}\n\nMantra: {word}\n\n{user_entry}",
        file_name=f"morare_{date_str}.txt",
        mime="text/plain"
    )
