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
def make_hashes(password): return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password, hashed_text): return make_hashes(password) == hashed_text

# --- UI CONFIG ---
st.set_page_config(page_title="Morare | Your Private Vault", page_icon="📜", layout="centered")

# --- IMMERSIVE JOURNAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;1,400&family=Inter:wght@300;400&display=swap');

    /* The "Old World" Aesthetic */
    .stApp {
        background: radial-gradient(circle, #fdfcf0 0%, #f2efe2 100%);
    }

    /* Journal Book UI */
    .journal-page {
        background: #fffdfa;
        padding: 50px;
        border-radius: 5px;
        box-shadow: 
            5px 5px 20px rgba(0,0,0,0.05),
            inset 0 0 100px rgba(220,210,190,0.2);
        border: 1px solid #dcd1be;
        margin-bottom: 30px;
        position: relative;
    }

    /* The Spine Shadow */
    .journal-page::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 30px;
        background: linear-gradient(to right, rgba(0,0,0,0.05), transparent);
    }

    h1, h2, .brand {
        font-family: 'Playfair Display', serif;
        color: #2c2c2c;
    }

    .mantra-text {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 2.2rem;
        text-align: center;
        color: #5d5d5d;
        margin: 20px 0;
    }

    /* Paper Lines */
    div[data-baseweb="textarea"] {
        background-color: transparent !important;
        border: none !important;
    }
    textarea {
        background: repeating-linear-gradient(transparent, transparent 31px, #e5e5e5 32px) !important;
        line-height: 32px !important;
        font-family: 'Lora', serif !important;
        font-size: 1.1rem !important;
        color: #3b3b3b !important;
        padding-left: 10px !important;
    }

    /* Buttons Styling */
    .stButton>button {
        background-color: #4a4a4a;
        color: white;
        border-radius: 0px;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none;
        padding: 10px 25px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #9A8C98;
        color: white;
    }

    /* Archive Grid */
    .archive-card {
        background: #eeebe3;
        padding: 15px;
        border: 1px solid #d1cdbf;
        cursor: pointer;
        transition: 0.2s;
        font-family: 'Lora', serif;
    }
    .archive-card:hover { background: #e5e2d6; }
    </style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION LOGIC ---
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

def auth_screen():
    st.markdown("<h1 style='text-align:center;'>Morare</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Sign In", "Open New Vault"])
    
    with tab1:
        user = st.text_input("Username", key="login_user")
        pw = st.text_input("Password", type="password", key="login_pw")
        if st.button("Enter Vault"):
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
        new_user = st.text_input("Choose Username")
        new_pw = st.text_input("Choose Password", type="password")
        if st.button("Create Vault"):
            try:
                c = conn.cursor()
                c.execute('INSERT INTO users(username,password) VALUES (?,?)', (new_user, make_hashes(new_pw)))
                conn.commit()
                st.success("Vault Created. You may now sign in.")
            except:
                st.error("This username is already claimed.")

# --- MAIN APP INTERFACE ---
def main_app():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state['username']}")
        page = st.radio("Navigate", ["Today's Reflection", "The Grand Library", "Account Settings"])
        if st.button("Close Vault"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- PAGE: TODAY'S REFLECTION ---
    if page == "Today's Reflection":
        # Load your content logic here (Simplified for the example)
        today = datetime.date.today().strftime("%Y-%m-%d")
        
        st.markdown(f"<div class='date-label' style='text-align:center;'>{datetime.date.today().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center;'>Morning Ink</h1>", unsafe_allow_html=True)
        
        # This part pulls from your content.js logic
        word = "Courage" 
        question = "If you had 20% more courage today, what would you do differently?"
        
        st.markdown(f"<div class='mantra-text'>{word}</div>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown(f"""
                <div class="journal-page">
                    <div style="font-family:'Lora'; font-style:italic; font-size:1.3rem; margin-bottom:20px; text-align:center;">
                        {question}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Writing Space
            entry = st.text_area("Your Soul's Draft", height=400, label_visibility="collapsed")
            
            if st.button("Seal Today's Entry"):
                c = conn.cursor()
                # Check if entry exists for today
                c.execute('SELECT * FROM journal WHERE username=? AND date=?', (st.session_state['username'], today))
                if c.fetchone():
                    c.execute('UPDATE journal SET content=? WHERE username=? AND date=?', (entry, st.session_state['username'], today))
                else:
                    c.execute('INSERT INTO journal(username, date, content, word, question) VALUES (?,?,?,?,?)', 
                              (st.session_state['username'], today, entry, word, question))
                conn.commit()
                st.balloons()
                st.success("Your thoughts have been safely locked in the vault.")

    # --- PAGE: THE GRAND LIBRARY ---
    elif page == "The Grand Library":
        st.markdown("<h1>The Grand Library</h1>", unsafe_allow_html=True)
        st.write("Click on a past date to reopen the book of your memories.")
        
        c = conn.cursor()
        c.execute('SELECT date, word, content, question FROM journal WHERE username=? ORDER BY date DESC', (st.session_state['username'],))
        entries = c.fetchall()
        
        if not entries:
            st.info("The library is currently empty. Write your first page today.")
        else:
            for row in entries:
                with st.expander(f"📖 {row[0]} — Mantra: {row[1]}"):
                    st.markdown(f"""
                    <div class="journal-page" style="box-shadow:none; border: 1px solid #eee;">
                        <p><strong>Prompt:</strong> <em>{row[3]}</em></p>
                        <hr>
                        <p style="font-family:'Lora'; white-space: pre-wrap;">{row[2]}</p>
                    </div>
                    """, unsafe_allow_html=True)

# --- ROUTING ---
if not st.session_state['logged_in']:
    auth_screen()
else:
    main_app()
