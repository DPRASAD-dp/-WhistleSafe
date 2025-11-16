# user_input.py
import streamlit as st
import sqlite3
from pathlib import Path
from lingo_translation import translate, LANGUAGES

# -------------------------
# Ensure upload folder exists
# -------------------------
Path("uploads").mkdir(exist_ok=True)

# -------------------------
# Language Selector
# -------------------------
selected_language = st.sidebar.selectbox(
    "🌐 Select Language",
    list(LANGUAGES.keys())
)
TARGET_LANG = LANGUAGES[selected_language]

# -------------------------
# Theming (CSS)
# -------------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #1e3c72, #2a5298);
    }
    .css-1d391kg, .css-12oz5g7 {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background-color: #2e5cb8;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #3d7be3;
    }
    h1, h2, h3 {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# DATABASE SETUP
# -------------------------
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    video_path TEXT,
    text_report TEXT,
    status TEXT DEFAULT 'Pending',
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
''')

conn.commit()

# -------------------------
# Dummy Users (For Testing)
# -------------------------
dummy_users = [
    {'username': 'reporter1', 'password': 'password1'},
    {'username': 'reporter2', 'password': 'password2'},
    {'username': 'reporter3', 'password': 'password3'},
    {'username': 'reporter4', 'password': 'password4'}
]

for user in dummy_users:
    cursor.execute(
        'INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)',
        (user['username'], user['password'])
    )
conn.commit()


# -------------------------
# Helper Functions
# -------------------------
def authenticate(username, password):
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?',
        (username, password)
    )
    return cursor.fetchone()


def save_upload(user_id, video_path, text_report):
    cursor.execute(
        'INSERT INTO uploads (user_id, video_path, text_report) VALUES (?, ?, ?)',
        (user_id, video_path, text_report)
    )
    conn.commit()


def get_user_reports(user_id):
    cursor.execute(
        'SELECT video_path, text_report, status FROM uploads WHERE user_id = ?',
        (user_id,)
    )
    return cursor.fetchall()


# -------------------------
# Title
# -------------------------
st.title(translate("WhistleSafe : Anonymous Reporting System", TARGET_LANG))

# -------------------------
# SESSION STATE INIT
# -------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None

# -------------------------
# LOGIN PAGE
# -------------------------
if not st.session_state.authenticated:

    with st.form("login_form"):
        username = st.text_input(translate("Username", TARGET_LANG))
        password = st.text_input(translate("Password", TARGET_LANG), type="password")
        submit = st.form_submit_button(translate("Login", TARGET_LANG))

    if submit:
        user = authenticate(username, password)
        if user:
            st.session_state.authenticated = True
            st.session_state.user_id = user[0]
            st.success(translate("Logged in successfully!", TARGET_LANG))
            st.rerun()
        else:
            st.error(translate("Invalid username or password", TARGET_LANG))

else:
    # -------------------------
    # USER DASHBOARD
    # -------------------------
    st.sidebar.title(translate("User Dashboard", TARGET_LANG))

    option = st.sidebar.selectbox(
        translate("Choose an option", TARGET_LANG),
        [
            translate("Check Progress", TARGET_LANG),
            translate("Upload Report", TARGET_LANG)
        ]
    )

    # -------------------------
    # CHECK PROGRESS
    # -------------------------
    if option == translate("Check Progress", TARGET_LANG):
        st.header(translate("Previous Reports", TARGET_LANG))

        reports = get_user_reports(st.session_state.user_id)

        if reports:
            for idx, report in enumerate(reports):
                st.write(f"{translate('Report', TARGET_LANG)} {idx + 1}:")

                video_path = Path(report[0])
                if video_path.exists():
                    st.video(str(video_path))
                else:
                    st.warning(
                        translate("Video file not found at:", TARGET_LANG) + " " + report[0]
                    )

                # The stored report is already translated to English before saving.
                st.text(report[1])
                st.write(f"{translate('Status', TARGET_LANG)}: {translate(report[2], TARGET_LANG)}")
        else:
            st.info(translate("No reports found.", TARGET_LANG))

    # -------------------------
    # UPLOAD REPORT
    # -------------------------
    elif option == translate("Upload Report", TARGET_LANG):

        st.header(translate("Upload New Report", TARGET_LANG))

        video_file = st.file_uploader(
            translate("Upload Video", TARGET_LANG),
            type=["mp4", "mov", "avi"]
        )

        text_report = st.text_area(
            translate("Enter Report Text", TARGET_LANG)
        )

        if st.button(translate("Submit Report", TARGET_LANG)):
            if video_file and text_report:

                # Save the video file
                video_path = Path("uploads") / video_file.name
                with open(video_path, "wb") as f:
                    f.write(video_file.getbuffer())

                # Convert user text to English for processing pipeline
                english_report = translate(text_report, "en")

                save_upload(
                    st.session_state.user_id,
                    str(video_path),
                    english_report
                )

                st.success(translate("Report uploaded successfully!", TARGET_LANG))
            else:
                st.warning(
                    translate("Please upload a video and enter a report text.", TARGET_LANG)
                )

    # -------------------------
    # LOGOUT BUTTON
    # -------------------------
    if st.sidebar.button(translate("Logout", TARGET_LANG)):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.rerun()