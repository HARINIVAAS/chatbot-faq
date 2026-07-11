import streamlit as st
from chatbot import get_answer

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Apple iPhone Product Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# SESSION STATE
# ======================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ======================================================
# CSS
# ======================================================

st.markdown("""
<style>

/* Hide Streamlit chrome */
#MainMenu, header, footer { visibility: hidden; }

/* App background */
.stApp {
    background: #F7F8FA;
}

/* Font */
html, body, [class*="css"] {
    font-family: "Segoe UI", Inter, Arial, sans-serif;
    color: #111827;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-bottom: 2rem;
    max-width: 1180px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

section[data-testid="stSidebar"] h1 {
    font-size: 26px;
    font-weight: 700;
    color: #111827;
}

section[data-testid="stSidebar"] p {
    font-size: 14px;
    color: #6B7280;
}

section[data-testid="stSidebar"] h4 {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-top: 6px;
}

/* Sidebar topic buttons -> look like a nav list, not pill buttons.
   Scoped to the "sidebar_nav" container only, so it doesn't clash
   with the Clear Chat button below it. */
.st-key-sidebar_nav div[data-testid="stButton"] > button {
    width: 100%;
    background: transparent !important;
    border: none !important;
    color: #374151 !important;
    font-size: 14.5px;
    font-weight: 500;
    text-align: left;
    padding: 8px 10px;
    border-radius: 8px;
    box-shadow: none !important;
    transition: .15s;
}

.st-key-sidebar_nav div[data-testid="stButton"] > button:hover {
    background: #EFF6FF !important;
    color: #2563EB !important;
}

/* Clear Chat: its own outline / danger style, kept readable */
.st-key-clear_chat div[data-testid="stButton"] > button {
    width: 100%;
    height: 42px;
    background: #FFFFFF !important;
    border: 1px solid #FCA5A5 !important;
    color: #DC2626 !important;
    font-size: 14px;
    font-weight: 600;
    box-shadow: none !important;
}

.st-key-clear_chat div[data-testid="stButton"] > button:hover {
    background: #FEF2F2 !important;
    border-color: #EF4444 !important;
    color: #DC2626 !important;
    transform: none !important;
}

/* Hero card */
.hero {
    background: #FFFFFF;
    padding: 40px;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(0,0,0,.05);
    margin-bottom: 25px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.hero-title {
    font-size: 42px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 12px;
    line-height: 1.2;
}

.hero-sub {
    font-size: 17px;
    color: #6B7280;
    line-height: 1.7;
    margin-bottom: 0;
}

.hero-image-card {
    background: #FFFFFF;
    border-radius: 18px;
    box-shadow: 0 5px 18px rgba(0,0,0,.05);
    padding: 24px 24px 0 24px;
    height: 100%;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    overflow: hidden;
}

/* Section headers */
.section-header {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: .05em;
    text-transform: uppercase;
    color: #6B7280;
    margin: 4px 0 14px 2px;
}

/* Search input */
div[data-testid="stTextInput"] input {
    height: 56px;
    border-radius: 12px;
    border: 1px solid #D1D5DB;
    background: #FFFFFF;
    font-size: 16px;
    color: #111827;
    padding-left: 16px;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #2563EB;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, .15);
}

/* Buttons (search + topic pills in main area) */
div[data-testid="stButton"] > button,
div[data-testid="stFormSubmitButton"] > button {
    width: 100%;
    height: 56px;
    background: #2563EB;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    transition: .2s;
    box-shadow: 0 2px 8px rgba(37,99,235,.25);
}

div[data-testid="stButton"] > button:hover,
div[data-testid="stButton"] > button:focus,
div[data-testid="stButton"] > button:active,
div[data-testid="stFormSubmitButton"] > button:hover,
div[data-testid="stFormSubmitButton"] > button:focus,
div[data-testid="stFormSubmitButton"] > button:active {
    background: #1D4ED8 !important;
    color: white !important;
    box-shadow: 0 4px 14px rgba(37,99,235,.35);
    transform: translateY(-1px);
}

/* Popular search chips: icon pills with lift + glow hover */
.chip-row div[data-testid="stButton"] > button {
    height: 46px;
    background: #FFFFFF;
    color: #374151;
    border: 1px solid #E5E7EB;
    border-radius: 25px;
    font-size: 14.5px;
    font-weight: 600;
    box-shadow: 0 2px 6px rgba(0,0,0,.03);
    transition: .22s ease;
}

.chip-row div[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #EFF6FF, #F5F9FF);
    color: #2563EB;
    border-color: #93C5FD;
    box-shadow: 0 8px 20px rgba(37,99,235,.18);
    transform: translateY(-3px) scale(1.03);
}

/* Chat bubbles (custom, replaces st.chat_message for animation control) */
.chat-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 18px;
    animation: floatIn .5s ease-out;
}

.user-row {
    flex-direction: row-reverse;
}

.chat-avatar {
    width: 38px;
    height: 38px;
    min-width: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 10px rgba(0,0,0,.08);
    animation: floatBob 3s ease-in-out infinite;
}

.assistant-avatar { background: linear-gradient(135deg,#DBEAFE,#EFF6FF); }
.user-avatar { background: linear-gradient(135deg,#DCFCE7,#F0FDF4); }

.chat-bubble {
    max-width: 74%;
    padding: 14px 18px;
    border-radius: 16px;
    box-shadow: 0 3px 10px rgba(0,0,0,.05);
    border: 1px solid #F1F5F9;
    background: #FFFFFF;
}

.user-bubble {
    background: #2563EB;
    color: #FFFFFF;
    border: none;
}

.bubble-label {
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .05em;
    margin-bottom: 4px;
    opacity: .65;
}

.user-bubble .bubble-label { color: #EFF6FF; opacity: .85; }

.bubble-text {
    font-size: 16px;
    line-height: 1.75;
    color: #374151;
}

.user-bubble .bubble-text { color: #FFFFFF; }

/* Typing indicator */
.typing-bubble {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 16px 20px;
}

.typing-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #93C5FD;
    animation: bounceDot 1.2s infinite ease-in-out;
}

.typing-dot:nth-child(2) { animation-delay: .15s; }
.typing-dot:nth-child(3) { animation-delay: .3s; }

@keyframes floatIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes floatBob {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-4px); }
}

@keyframes bounceDot {
    0%, 80%, 100% { transform: translateY(0); opacity: .5; }
    40%           { transform: translateY(-6px); opacity: 1; }
}

/* Empty state */
.empty-state {
    margin-top: 50px;
    text-align: center;
    color: #9CA3AF;
    font-size: 16px;
}

/* Footer */
.app-footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #E5E7EB;
    text-align: center;
    font-size: 14px;
    color: #9CA3AF;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HELPERS
# ======================================================

def ask(question_text: str):
    """Run the chatbot on a question and store the exchange."""
    answer = get_answer(question_text)
    st.session_state.chat_history.append(("You", question_text))
    st.session_state.chat_history.append(("Assistant", answer))


# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("Apple")
st.sidebar.markdown("### Product Assistant")
st.sidebar.divider()
st.sidebar.markdown("#### Popular Topics")

topics = [
    "iPhone 16",
    "iPhone 16 Pro",
    "iPhone 16 Pro Max",
    "Camera",
    "Battery",
    "Charging",
    "Apple Intelligence",
    "Compare Models",
]

with st.sidebar.container(key="sidebar_nav"):
    for topic in topics:
        if st.button(topic, key=f"sidebar_{topic}"):
            st.session_state.pending_question = topic

st.sidebar.divider()

with st.sidebar.container(key="clear_chat"):
    if st.button("Clear Chat"):
        st.session_state.chat_history = []

# ======================================================
# HERO SECTION
# ======================================================

left, right = st.columns([2.3, 1], gap="large")

with left:
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Apple iPhone Product Assistant</div>
        <div class="hero-sub">
        Find accurate information about iPhone models, camera features,
        battery life, performance, Apple Intelligence, storage options
        and model comparisons.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="hero-image-card">', unsafe_allow_html=True)
    st.image("images/iphone16.png", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ======================================================
# QUICK TOPICS (now functional)
# ======================================================

st.markdown('<div class="section-header">Popular Searches</div>', unsafe_allow_html=True)

st.markdown('<div class="chip-row">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
quick_topics = [
    ("📱", "iPhone 16"),
    ("📷", "Camera"),
    ("🔋", "Battery"),
    ("⚖️", "Compare Models"),
]
for col, (icon, label) in zip((c1, c2, c3, c4), quick_topics):
    with col:
        if st.button(f"{icon}  {label}", key=f"chip_{label}"):
            st.session_state.pending_question = label
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# ======================================================
# SEARCH BAR
# ======================================================

st.markdown('<div class="section-header">Ask a Question</div>', unsafe_allow_html=True)

with st.form(key="ask_form", clear_on_submit=True):
    search_col, button_col = st.columns([5, 1], vertical_alignment="bottom")

    with search_col:
        question = st.text_input(
            "Ask a question",
            placeholder="Example: Compare iPhone 16 and iPhone 16 Pro",
            label_visibility="collapsed",
        )

    with button_col:
        search = st.form_submit_button("Search")

    if search:
        if question.strip() == "":
            st.warning("Please enter a question.")
        else:
            st.session_state.pending_question = question.strip()

# ======================================================
# RUN PENDING QUESTION (from search box, chip, or sidebar topic)
# ======================================================

if st.session_state.pending_question:
    q = st.session_state.pending_question
    st.session_state.pending_question = None

    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="chat-row">
        <div class="chat-avatar assistant-avatar">📱</div>
        <div class="chat-bubble typing-bubble">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ask(q)
    typing_placeholder.empty()

st.write("")
st.markdown("---")
st.write("")

# ======================================================
# CHAT SECTION
# ======================================================

if st.session_state.chat_history:
    st.markdown("## Conversation")

    for sender, message in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"""
            <div class="chat-row user-row">
                <div class="chat-avatar user-avatar">🙂</div>
                <div class="chat-bubble user-bubble">
                    <div class="bubble-label">You</div>
                    <div class="bubble-text">{message}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-row assistant-row">
                <div class="chat-avatar assistant-avatar">📱</div>
                <div class="chat-bubble assistant-bubble">
                    <div class="bubble-label">Apple Assistant</div>
                    <div class="bubble-text">{message}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown(
        '<div class="empty-state">Start a conversation by asking a question '
        'about any iPhone model.</div>',
        unsafe_allow_html=True,
    )

# ======================================================
# SPACING
# ======================================================

st.write("")
st.write("")
st.write("")

# ======================================================
# FOOTER
# ======================================================

st.markdown(
    '<div class="app-footer">Apple iPhone Product Assistant</div>',
    unsafe_allow_html=True,
)