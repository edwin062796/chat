import streamlit as st
import time

# --------------------------
# Chatbot logic
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()

    if user_message in ["hi", "hello", "hey", "start"]:
        return "👋 Hello! How can I assist you today?"

    elif "program registration" in user_message or user_message == "1":
        return "📝 You can register for TESDA programs through the Unified TVET Program Registration and Accreditation System (UTPRAS)."

    elif "courses" in user_message or user_message == "2":
        return "📚 You can explore the available online courses here: https://e-tesda.gov.ph/course"

    elif "contact" in user_message or user_message == "3":
        return "📞 You can reach us via email at **ncr.quezoncity@tesda.gov.ph** or call **8353-8161**. Our office is open Monday–Friday, 8:00 AM to 5:00 PM."
        
    elif "requirements" in user_message or user_message == "4":
        return "📋 You can check the requirements for program registration here: (insert link)."

    else:
        return "❓ Sorry, I didn’t understand that. Please select an option below or type 'help'."

# --------------------------
# Page setup
# --------------------------
st.set_page_config(page_title="TESDA QC UTPRAS Chatbot", page_icon="🤖", layout="wide")

# --------------------------
# Sidebar functions
# --------------------------
with st.sidebar:
    st.title("⚙️ Chatbot Settings")

    # Dark mode toggle
    dark_mode = st.checkbox("🌙 Enable Dark Mode")

    # Help menu expander
    with st.expander("❓ Help & Commands"):
        st.markdown("""
        - 👋 **Hello** → Start a greeting  
        - 📝 **Program Registration** → Learn how to register  
        - 📚 **Courses** → Explore available TESDA courses  
        - 📋 **Requirements** → View needed documents  
        - 📞 **Contact Us** → Get TESDA QC details  
        """)

    # Navigation buttons
    if st.button("⬆️ Scroll to Top"):
        st.markdown("<a href='#top'> </a>", unsafe_allow_html=True)
    if st.button("⬇️ Scroll to Bottom"):
        st.markdown("<a href='#bottom'> </a>", unsafe_allow_html=True)

    # Reset chat
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = [("Bot", "👋 Hello! Welcome to TESDA Quezon City UTPRAS Chatbot. Type 'help' to see available options.")]
        st.session_state.last_action = None
        st.experimental_rerun()

# --------------------------
# CSS (Light / Dark theme)
# --------------------------
light_css = """
    <style>
        body { background-color: #f9fafb; }
        .main-title { text-align: center; font-size: 2.5rem; color: #16a34a; font-weight: bold; margin-bottom: 10px; }
        .subtitle { text-align: center; font-size: 1.1rem; color: #555; margin-bottom: 30px; }
        .chat-bubble-user { background-color: #DCF8C6; padding: 12px 16px; border-radius: 20px; margin: 8px 0; text-align: right; max-width: 75%; margin-left: auto; font-size: 1rem; }
        .chat-bubble-bot { background-color: #E6E6FA; padding: 12px 16px; border-radius: 20px; margin: 8px 0; text-align: left; max-width: 75%; margin-right: auto; font-size: 1rem; }
    </style>
"""

dark_css = """
    <style>
        body { background-color: #1e1e2f; color: #eee; }
        .main-title { text-align: center; font-size: 2.5rem; color: #22c55e; font-weight: bold; margin-bottom: 10px; }
        .subtitle { text-align: center; font-size: 1.1rem; color: #ccc; margin-bottom: 30px; }
        .chat-bubble-user { background-color: #2a3f2d; color: #e2e2e2; padding: 12px 16px; border-radius: 20px; margin: 8px 0; text-align: right; max-width: 75%; margin-left: auto; font-size: 1rem; }
        .chat-bubble-bot { background-color: #2f2f4f; color: #e2e2e2; padding: 12px 16px; border-radius: 20px; margin: 8px 0; text-align: left; max-width: 75%; margin-right: auto; font-size: 1rem; }
    </style>
"""

st.markdown(dark_css if dark_mode else light_css, unsafe_allow_html=True)

# --------------------------
# Session state
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [("Bot", "👋 Hello! Welcome to TESDA Quezon City UTPRAS Chatbot. Type 'help' to see available options.")]

if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Main title
# --------------------------
st.markdown("<div id='top' class='main-title'>TESDA Quezon City UTPRAS</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Your assistant for program registration and inquiries</div>", unsafe_allow_html=True)

# --------------------------
# Quick action buttons
# --------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📝 Program Registration"):
        st.session_state.last_action = "program registration"
with col2:
    if st.button("📚 Courses"):
        st.session_state.last_action = "courses"
with col3:
    if st.button("📋 Requirements"):
        st.session_state.last_action = "requirements"
with col4:
    if st.button("📞 Contact Us"):
        st.session_state.last_action = "contact"

# --------------------------
# Input handling
# --------------------------
user_input = None

if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None

try:
    if user_input is None:
        chat_in = st.chat_input("Type your message here...")
        if chat_in:
            user_input = chat_in
except Exception:
    if user_input is None:
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("Type your message here:", value=st.session_state.typed_value, key="typed_value")
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("You", typed)):
            user_input = typed

# --------------------------
# Process chatbot response
# --------------------------
if user_input:
    st.session_state.messages.append(("You", user_input))
    with st.spinner("Bot is typing..."):
        time.sleep(0.7)
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An error occurred: {e}"
    st.session_state.messages.append(("Bot", bot_reply))
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display messages
# --------------------------
for role, msg in st.session_state.messages:
    if role == "You":
        st.markdown(f"<div class='chat-bubble-user'>🧑 <b>{role}:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>🤖 <b>{role}:</b> {msg}</div>", unsafe_allow_html=True)

st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)
