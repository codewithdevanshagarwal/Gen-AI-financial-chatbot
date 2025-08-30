import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# ---------------- ENV & API ----------------
load_dotenv()
API_URL = "http://127.0.0.1:8000"

# ========== CYBERPUNK CSS ==========
def add_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0a0f1a 0%, #1a2b3a 50%, #0a1a2a 100%);
        color: #c0d6e4;
        font-family: 'Roboto Mono', monospace;
        min-height: 100vh;
    }

    .frosted-glass {
        background: rgba(10, 15, 26, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid #00aaff44;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 170, 255, 0.1);
    }

    h1, h2, h3 {
        color: #00e0ff;
        font-weight: 700;
        text-shadow: 0 0 10px #00aaff88;
        margin-bottom: 1.5rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(10, 15, 26, 0.9);
        border-right: 1px solid #00aaff44;
    }

    /* ===== NAVIGATION (SIDEBAR) – MAKE ITEMS CLEAR ===== */

    /* Base color for all nav items (radio options) */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio label div,
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] .stRadio label span {
        color: #bfefff !important;   /* light neon cyan */
        opacity: 1 !important;
        font-weight: 650;
    }

    /* Hover state for nav items */
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover,
    [data-testid="stSidebar"] .stRadio label:hover *,
    [data-testid="stSidebar"] .stRadio label:hover {
        color: #00e0ff !important;
        text-shadow: 0 0 6px rgba(0,224,255,0.7);
    }

    /* Selected (active) nav item */
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"],
    [data-testid="stSidebar"] [role="radio"][aria-checked="true"] * {
        color: #00f7ff !important;         /* brighter cyan */
        font-weight: 800 !important;
        text-shadow: 0 0 6px rgba(0,224,255,0.95), 0 0 14px rgba(0,170,255,0.6);
    }

    /* Make the radio dot cyan as well (modern browsers) */
    [data-testid="stSidebar"] input[type="radio"] { accent-color: #00e0ff; }

    /* Sidebar headings / helper text */
    [data-testid="stSidebar"] :where(h2, h3, label, p, span) {
        color: #e6f7ff !important;
        opacity: 1 !important;
    }

    /* ===== EXISTING STYLES (unchanged) ===== */

    div.stButton > button {
        background: linear-gradient(135deg, #001a33 0%, #003366 100%);
        color: #00e0ff;
        border: 2px solid #00aaff;
        border-radius: 12px;
        padding: 0.75em 2em;
        font-weight: 700;
        font-family: 'Roboto Mono', monospace;
        box-shadow: 0 0 15px #00aaff, inset 0 0 10px #00aaff44;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #00aaff 0%, #00e0ff 100%);
        color: #001a33;
        box-shadow: 0 0 25px #00aaff, inset 0 0 20px #00aaff;
        transform: translateY(-2px);
    }

    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(0, 26, 51, 0.8);
        color: #c0d6e4;
        border: 2px solid #00aaff;
        border-radius: 10px;
        padding: 0.75rem;
        font-family: 'Roboto Mono', monospace;
        font-size: 1rem;
    }

    /* Main content widget labels */
    :where(.stTextInput, .stTextArea, .stNumberInput, .stSelectbox) label {
        color: #e6f7ff !important;
        opacity: 1 !important;
        font-weight: 600;
        text-shadow: 0 0 4px rgba(0, 224, 255, 0.35);
    }

    .response-box {
        background: rgba(0, 26, 51, 0.9);
        border: 1px solid #00aaff;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 170, 255, 0.15);
        white-space: pre-wrap;
    }

    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
        background: rgba(0, 26, 51, 0.4);
        border: 1px solid #00aaff44;
        border-radius: 15px;
        margin-bottom: 1rem;
    }

    .user-bubble {
        background: linear-gradient(135deg, #00aaff99, #00e0ffaa);
        color: #001a33;
        padding: 10px;
        border-radius: 12px;
        margin: 5px 0;
        max-width: 70%;
        float: right;
        clear: both;
    }

    .bot-bubble {
        background: rgba(0, 26, 51, 0.85);
        color: #c0d6e4;
        padding: 10px;
        border-radius: 12px;
        margin: 5px 0;
        max-width: 70%;
        float: left;
        clear: both;
        border: 1px solid #00aaff66;
    }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #001a33; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00aaff, #00e0ff);
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
# ========== API CALL ==========
def call_api(endpoint, payload):
    try:
        response = requests.post(f"{API_URL}/{endpoint}", json=payload, timeout=30)
        if response.ok:
            return response.json()
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Request failed: {e}")
        return None

# ========== MAIN APP ==========
def main():
    st.set_page_config(page_title="Personal Finance Chatbot", layout="wide", page_icon="🤖")
    add_custom_css()

    if "page" not in st.session_state: st.session_state.page = "home"
    if "chat_history" not in st.session_state: st.session_state.chat_history = []

    # ---- SIDEBAR NAVIGATION ----
    with st.sidebar:
        st.title("💼 Navigation")
        menu = {
            "🏠 Home": "home",
            "💬 Chat Assistant": "qa",
            "📊 Budget Summary": "budget",
            "🔍 Spending Insights": "spending",
            "📈 NLU Analysis": "nlu"
        }
        selected = st.radio("Choose Feature", list(menu.keys()))
        st.session_state.page = menu[selected]
        st.markdown("---")
        st.info("**AI Finance Assistant**\nAsk questions, analyze budgets, and get insights!")

    # ---- HOME ----
    if st.session_state.page == "home":
        st.title("🤖 Personal Finance Chatbot")
        st.markdown("""
        <div class="frosted-glass">
            <h3 style='text-align:center;'>💡 Your Cyberpunk Finance Assistant</h3>
            <p style='text-align:center;'>Ask questions, track spending, and analyze budgets with AI-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)

    # ---- CHAT ASSISTANT ----
    elif st.session_state.page == "qa":
        st.title("💬 Chat with Finance Assistant")
        persona = st.selectbox("Select Persona", ["student", "professional"])

        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for msg in st.session_state.chat_history:
            cls = "user-bubble" if msg["role"] == "user" else "bot-bubble"
            st.markdown(f"<div class='{cls}'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        user_input = st.text_input("Type your message:")
        if st.button("Send"):
            if user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Thinking..."):
                    result = call_api("generate", {"question": user_input, "persona": persona})
                    if result:
                        bot_reply = result.get("answer", "Sorry, couldn't process that.")
                        st.session_state.chat_history.append({"role": "bot", "content": bot_reply})
                st.experimental_rerun()

    # ---- BUDGET SUMMARY ----
    elif st.session_state.page == "budget":
        st.title("📊 Budget Summary Analysis")
        persona = st.selectbox("Persona", ["student", "professional"])
        income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=3000.0)
        savings_goal = st.number_input("Savings Goal ($)", min_value=0.0, step=50.0, value=500.0)

        expenses = {}
        for c in ["Rent", "Food", "Transportation", "Utilities", "Entertainment", "Shopping", "Healthcare"]:
            expenses[c] = st.number_input(f"{c} ($)", min_value=0.0, step=10.0, value=0.0, key=f"budget_{c}")

        if st.button("Generate Budget Summary"):
            payload = {"income": income, "savings_goal": savings_goal, "expenses": expenses, "persona": persona}
            with st.spinner("📈 Analyzing..."):
                res = call_api("budget-summary", payload)
                if res:
                    st.markdown(f"<div class='response-box'>{res.get('message','No summary')}</div>", unsafe_allow_html=True)

    # ---- SPENDING INSIGHTS ----
    elif st.session_state.page == "spending":
        st.title("🔍 Spending Insights")
        persona = st.selectbox("Persona", ["student", "professional"])
        income = st.number_input("Monthly Income ($)", min_value=0.0, step=100.0, value=3000.0)

        st.subheader("Financial Goals")
        goals = []
        for g in ["Emergency Fund", "Vacation", "Laptop"]:
            amt = st.number_input(f"{g} ($)", min_value=0.0, step=50.0, key=f"goal_{g}")
            if amt > 0:
                goals.append({"name": g, "amount": amt})

        st.subheader("Expenses")
        expenses = {}
        for e in ["Rent", "Food", "Transport", "Utilities", "Entertainment"]:
            expenses[e] = st.number_input(f"{e} ($)", min_value=0.0, step=10.0, value=0.0, key=f"spend_{e}")

        if st.button("Analyze Spending"):
            payload = {"income": income, "expenses": expenses, "goals": goals, "persona": persona}
            with st.spinner("🔬 Analyzing..."):
                res = call_api("spending-insights", payload)
                if res:
                    st.markdown(f"<div class='response-box'>{res.get('message','No insights')}</div>", unsafe_allow_html=True)

    # ---- NLU ANALYSIS ----
    elif st.session_state.page == "nlu":
        st.title("📈 Text Sentiment & Entity Analysis")
        text = st.text_area("Enter text for analysis:")
        if st.button("Analyze"):
            if text.strip():
                with st.spinner("Analyzing..."):
                    res = call_api("nlu", {"text": text})
                    if res:
                        st.markdown(f"<div class='response-box'>{res.get('nlu',{}).get('analysis','No result')}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

# cd C:\Users\adam\OneDrive\Desktop\personal-finance-chatbot\frontend\streamlit       
#PS C:\Users\adam\OneDrive\Desktop\personal-finance-chatbot\frontend\streamlit> & c:/Users/adam/OneDrive/Desktop/personal-finance-chatbot/.venv/Scripts/Activate.ps1
#(.venv) PS C:\Users\adam\OneDrive\Desktop\personal-finance-chatbot\frontend\streamlit> streamlit run app.py