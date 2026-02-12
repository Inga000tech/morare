import streamlit as st
import sqlite3
import datetime
import hashlib
import json
import re

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('morare_vault.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS journal (username TEXT, date TEXT, content TEXT, word TEXT, question TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- SECURITY ---
def make_hashes(password): 
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text): 
    return make_hashes(password) == hashed_text

# --- UI CONFIG ---
st.set_page_config(page_title="Morare", page_icon="📜", layout="centered")

# --- IMMERSIVE JOURNAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;1,400&family=Inter:wght@300;400&display=swap');

    .stApp { background: #f2efe2; }

    /* The Journal Page Look */
    .journal-page {
        background: #fffdfa;
        padding: 40px;
        border-radius: 2px;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #dcd1be;
        margin-bottom: 20px;
        position: relative;
    }
    
    /* Binding shadow */
    .journal-page::after {
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 15px;
        background: linear-gradient(to right, rgba(0,0,0,0.08), transparent);
    }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #2c2c2c; }
    p, span { font-family: 'Lora', serif; }

    .mantra-display {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 2.8rem;
        color: #5d5d5d;
        margin-bottom: 30px;
    }

    /* Styling the Lined Paper Input */
    textarea {
        background: repeating-linear-gradient(transparent, transparent 31px, #e5e5e5 32px) !important;
        line-height: 32px !important;
        font-family: 'Lora', serif !important;
        font-size: 1.15rem !important;
        color: #3b3b3b !important;
        border: none !important;
    }

    /* Center the login box */
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 30px;
        background: white;
        border-radius: 8px;
    }

    /* Hide UI clutter */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- CONTENT LOADER (Integrated for speed) ---
def get_daily_content():
    # Fallback content if content.js isn't found
    today_key = datetime.date.today().strftime("%Y-%m-%d")
    return {
        "word": "Clarity",
        "question": "What is one thing you are doing today purely because you want to?",
        "history": "Ernest Shackleton’s Endurance: After their ship was crushed by ice, he led his crew to safety over 800 miles of ocean.",
        "quote": "The best way out is always through. — Robert Frost"
    }

# --- AUTHENTICATION SCREENS ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def auth_flow():
    st.markdown("<h1 style='text-align:center;'>Morare</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Your Private Sanctuary</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Create Vault"])
    
    with tab1:
        user = st.text_input("Username", key="l_user")
        pw = st.text_input("Password", type="password", key="l_pw")
        if st.button("Open Vault"):
            c = conn.cursor()
            c.execute('SELECT password FROM users WHERE username =?', (user,))
            data = c.fetchone()
            if data and check_hashes(pw, data[0]):
                st.session_state['logged_in'] = True
                st.session_state['username'] = user
                st.rerun()
            else:
                st.error("The key does not fit this lock.")

    with tab2:
        new_user = st.text_input("New Username", key="r_user")
        new_pw = st.text_input("New Password", type="password", key="r_pw")
        if st.button("Forge Key"):
            if new_user and new_pw:
                try:
                    c = conn.cursor()
                    c.execute('INSERT INTO users(username,password) VALUES (?,?)', (new_user, make_hashes(new_pw)))
                    conn.commit()
                    st.success("Vault Created. You may now sign in.")
                except:
                    st.error("This username is already claimed.")
            else:
                st.warning("Please provide a name and a key.")

# --- MAIN APP ---
def main_app():
    user = st.session_state['username']
    
    with st.sidebar:
        st.markdown(f"### 🖋️ {user}")
        choice = st.radio("Navigation", ["Today's Ink", "The Archive", "Logout"])
        
    if choice == "Logout":
        st.session_state['logged_in'] = False
        st.rerun()

    data = get_daily_content()

    if choice == "Today's Ink":
        st.markdown(f"<div class='mantra-display'>{data['word']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="journal-page">
                <p style="text-align:center; color:#9A8C98; font-size:0.8rem; letter-spacing:2px;">{datetime.date.today().strftime('%A, %B %d')}</p>
                <h3 style="text-align:center; font-style:italic; margin-top:10px;">“{data['question']}”</h3>
                <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                <p style="font-size:0.85rem; color:#888;"><b>Historical Inspiration:</b> {data['history']}</p>
            </div>
        """, unsafe_allow_html=True)

        # Load existing entry if it exists
        c = conn.cursor()
        today_date = datetime.date.today().strftime("%Y-%m-%d")
        c.execute('SELECT content FROM journal WHERE username=? AND date=?', (user, today_date))
        existing = c.fetchone()
        
        val = existing[0] if existing else ""
        entry = st.text_area("Write...", value=val, height=450, label_visibility="collapsed")
        
        if st.button("Seal the Page"):
            if existing:
                c.execute('UPDATE journal SET content=? WHERE username=? AND date=?', (entry, user, today_date))
            else:
                c.execute('INSERT INTO journal(username, date, content, word, question) VALUES (?,?,?,?,?)', 
                          (user, today_date, entry, data['word'], data['question']))
            conn.commit()
            st.toast("Locked in the vault.")

    elif choice == "The Archive":
        st.markdown("<h1>The Grand Library</h1>", unsafe_allow_html=True)
        c = conn.cursor()
        c.execute('SELECT date, word, content FROM journal WHERE username=? ORDER BY date DESC', (user,))
        rows = c.fetchall()
        
        for r in rows:
            with st.expander(f"📖 {r[0]} — {r[1]}"):
                st.markdown(f"""
                <div class="journal-page">
                    <p style="white-space: pre-wrap; font-family:'Lora';">{r[2]}</p>
                </div>
                """, unsafe_allow_html=True)

# --- EXECUTION ---
if not st.session_state['logged_in']:
    auth_flow()
else:
    main_app()
