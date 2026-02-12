import streamlit as st
import sqlite3
import datetime
import hashlib
import json
import re
import os

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('morare_vault.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS journal (username TEXT, date TEXT, content TEXT, word TEXT, question TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- SECURITY UTILS ---
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# --- DATA PARSER ---
def load_morare_data():
    """Reads the content.js file to pull astrology, history, prompts, and quotes."""
    try:
        with open('content.js', 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Helper to extract JS arrays/objects via Regex
        def extract_list(var_name):
            match = re.search(rf'{var_name} = \[(.*?)\];', js_content, re.DOTALL)
            if match:
                items = re.findall(r'"(.*?)"', match.group(1))
                return items
            return []

        # Extract Astrology (simplified for Python)
        astro_match = re.search(r'astrologyEvents2026 = (\{.*?\});', js_content, re.DOTALL)
        astro_dict = {}
        if astro_match:
            # Clean up the JS to be JSON-like
            clean_js = re.sub(r'(\w+):', r'"\1":', astro_match.group(1))
            clean_js = re.sub(r',\s*\}', '}', clean_js)
            astro_dict = json.loads(clean_js)

        return {
            "events": astro_dict,
            "questions": extract_list("dailyQuestions"),
            "history": extract_list("historicalInspirations"),
            "quotes": extract_list("poeticQuotes")
        }
    except:
        return {"events": {}, "questions": ["What is on your heart today?"], "history": ["Resilience is human."], "quotes": ["Live fully."]}

# --- UI / UX DESIGN (Old Book Aesthetics) ---
st.set_page_config(page_title="Morare", page_icon="📜", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;1,400&family=Inter:wght@300;400;500&display=swap');

    /* The 'Safe Space' Palette */
    .stApp { background-color: #F4F1EA; } /* Aged paper background */

    .main .block-container { max-width: 650px; padding-top: 2rem; }

    /* The Journal Page Structure */
    .paper-sheet {
        background: #fffdfa;
        padding: 60px 50px;
        border-radius: 2px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.03), 0 0 40px rgba(0,0,0,0.02) inset;
        border: 1px solid #DCD1BE;
        margin-bottom: 2rem;
        position: relative;
    }

    /* Spine Shadow for 'Book' feel */
    .paper-sheet::before {
        content: ""; position: absolute; top: 0; left: 0; bottom: 0; width: 40px;
        background: linear-gradient(to right, rgba(0,0,0,0.06), transparent);
    }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #2C2C2C; }
    .mantra { font-family: 'Playfair Display', serif; font-style: italic; font-size: 3rem; text-align: center; color: #4A4A4A; margin-bottom: 10px; }
    .date-label { font-family: 'Inter', sans-serif; text-transform: uppercase; letter-spacing: 3px; font-size: 0.75rem; color: #9A8C98; text-align: center; }

    /* Styled Paper Lines for Input */
    div[data-baseweb="textarea"] { background: transparent !important; border: none !important; }
    textarea {
        background: repeating-linear-gradient(transparent, transparent 34px, #E8E2D5 35px) !important;
        line-height: 35px !important;
        font-family: 'Lora', serif !important;
        font-size: 1.2rem !important;
        color: #3B3B3B !important;
        padding-top: 8px !important;
        border: none !important;
    }

    .info-box { font-family: 'Inter', sans-serif; font-size: 0.9rem; color: #6B6B6B; line-height: 1.6; border-top: 1px solid #EEEBDD; padding-top: 20px; margin-top: 20px; }
    .quote-footer { font-family: 'Lora', serif; font-style: italic; color: #9A8C98; text-align: center; padding: 40px 0; font-size: 1.1rem; }

    /* Sidebar and Auth UI */
    .stSidebar { background-color: #EBE7DD !important; border-right: 1px solid #DCD1BE; }
    header, footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- APP LOGIC ---
data = load_morare_data()
today_obj = datetime.date.today()
date_str = today_obj.strftime("%Y-%m-%d")
day_idx = today_obj.timetuple().tm_yday

# Determine Content
event = data['events'].get(date_str, {"word": "Stillness", "title": "Integration", "meaning": "A quiet day for the soul."})
word = event.get('word', 'Presence')
question = data['questions'][day_idx % len(data['questions'])]
history = data['history'][day_idx % len(data['history'])]
quote = data['quotes'][day_idx % len(data['quotes'])]

# --- GUEST-FIRST DISPLAY ---
st.markdown(f'<div class="date-label">{today_obj.strftime("%A, %B %d")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="mantra">{word}</div>', unsafe_allow_html=True)

# THE PAPER INTERFACE
st.markdown(f"""
    <div class="paper-sheet">
        <h3 style="text-align:center; margin-bottom:30px;">“{question}”</h3>
        <div class="info-box">
            <strong>Today's Transit:</strong> {event['title']}<br>
            <span style="font-style:italic;">{event['meaning']}</span>
        </div>
        <div class="info-box" style="border:none;">
            <strong>Echoes of Humanity:</strong> {history}
        </div>
    </div>
""", unsafe_allow_html=True)

# Writing Area (Always Visible)
user_text = st.text_area("Write...", placeholder="Begin your journey here...", height=400, label_visibility="collapsed")

# --- ACCOUNT / PERSISTENCE LAYER ---
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Sidebar for Login/Signup
with st.sidebar:
    st.markdown("### Your Private Vault")
    if st.session_state['user'] is None:
        auth_mode = st.radio("Access", ["Guest Mode", "Sign In", "Create Vault"])
        
        if auth_mode == "Sign In":
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Unlock"):
                c = conn.cursor()
                c.execute('SELECT password FROM users WHERE username=?', (u,))
                row = c.fetchone()
                if row and check_hashes(p, row[0]):
                    st.session_state['user'] = u
                    st.rerun()
                else: st.error("Incorrect key.")
        
        elif auth_mode == "Create Vault":
            new_u = st.text_input("New Username")
            new_p = st.text_input("New Password", type="password")
            if st.button("Forge Vault"):
                try:
                    c = conn.cursor()
                    c.execute('INSERT INTO users VALUES (?,?)', (new_u, make_hashes(new_p)))
                    conn.commit()
                    st.success("Vault created. Switch to Sign In.")
                except: st.error("Name taken.")
    else:
        st.write(f"Logged in as: **{st.session_state['user']}**")
        nav = st.selectbox("Library", ["Today", "The Archive"])
        if st.button("Lock Vault (Logout)"):
            st.session_state['user'] = None
            st.rerun()

# --- SAVING LOGIC ---
if st.button("Save Reflection"):
    if st.session_state['user']:
        c = conn.cursor()
        c.execute('SELECT * FROM journal WHERE username=? AND date=?', (st.session_state['user'], date_str))
        if c.fetchone():
            c.execute('UPDATE journal SET content=? WHERE username=? AND date=?', (user_text, st.session_state['user'], date_str))
        else:
            c.execute('INSERT INTO journal VALUES (?,?,?,?,?)', (st.session_state['user'], date_str, user_text, word, question))
        conn.commit()
        st.success("Safely stored in your vault.")
    else:
        st.info("💡 You are in Guest Mode. Your writing will stay until you refresh, but to save it permanently, create a Vault in the sidebar.")

# Archive View (Only if logged in)
if st.session_state['user'] and 'nav' in locals() and nav == "The Archive":
    st.markdown("---")
    st.markdown("### The Grand Library")
    c = conn.cursor()
    c.execute('SELECT date, content, word FROM journal WHERE username=? ORDER BY date DESC', (st.session_state['user'],))
    for row in c.fetchall():
        with st.expander(f"📜 {row[0]} | Mantra: {row[2]}"):
            st.markdown(f'<div class="paper-sheet" style="padding:20px; box-shadow:none; border-color:#eee;">{row[1]}</div>', unsafe_allow_html=True)

st.markdown(f'<div class="quote-footer">"{quote}"</div>', unsafe_allow_html=True)
