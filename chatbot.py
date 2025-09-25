import streamlit as st
import time

# --------------------------
# Simple rule-based chatbot function
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()

    if user_message in ["hi", "hello", "hey", "kumusta", "simula", "umpisa"]:
        return "👋 Magandang araw! Paano ka namin matutulungan?"

    elif "rehistro" in user_message or user_message == "1":
        return "📝 Maaari kang magparehistro sa TESDA program gamit ang Unified TVET Program Registration and Accreditation System (UTPRAS)."

    elif "kurso" in user_message or user_message == "2":
        return "📚 Narito ang listahan ng mga kurso na maaari mong tuklasin: https://e-tesda.gov.ph/course"

    elif "kausapin" in user_message or user_message == "3":
        return "📞 Maaari kang makipag-ugnayan sa amin sa pamamagitan ng email: ncr.quezoncity@tesda.gov.ph o tumawag sa 8353-8161. Bukas ang aming opisina Lunes–Biyernes, 8:00 AM – 5:00 PM."
        
    elif "requirements" in user_message or "pangailangan" in user_message or user_message == "4":
        return "📋 Maaari mong tingnan ang mga kinakailangan para sa program registration dito: (ilagay ang link)."

    else:
        return "❓ Paumanhin, hindi ko naintindihan ang iyong mensahe. Pumili sa mga opsyon sa ibaba o i-type ang 'tulong'."

# --------------------------
# Page config and session
# --------------------------
st.set_page_config(page_title="Chatbot: TESDA QC UTPRAS", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [("Bot", "👋 Kumusta! Maligayang pagdating sa TESDA Quezon City UTPRAS Chatbot. I-type ang 'tulong' upang makita ang mga opsyon.")]

if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Sidebar info + reset
# --------------------------
with st.sidebar:
    st.title("ℹ️ Tungkol sa Chatbot")
    st.write("Ito ay isang **simpleng rule-based chatbot** gamit ang Streamlit. Maaari mong gawin ang mga sumusunod:")
    st.markdown("""
    - 👋 Pagati  
    - 📝 Program Registration  
    - 📚 Listahan ng Kurso  
    - 📋 Mga Kinakailangan  
    - 📞 Makipag-ugnayan  
    """)
    if st.button("🔄 I-reset ang Chat"):
        st.session_state.messages = [("Bot", "👋 Kumusta! Maligayang pagdating sa TESDA Quezon City UTPRAS Chatbot. I-type ang 'tulong' upang makita ang mga opsyon.")]
        st.session_state.last_action = None
        st.experimental_rerun()

# --------------------------
# Title
# --------------------------
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>TESDA Quezon City UTPRAS</h1>", unsafe_allow_html=True)
st.write("Makipag-usap sa chatbot sa pamamagitan ng pag-type o pagpili ng mabilis na opsyon sa ibaba.")

# --------------------------
# Quick action buttons
# --------------------------
col1, col2, col3, col4 = st.columns(4)
if col1.button("📝 Program Registration"):
    st.session_state.last_action = "rehistro"
if col2.button("📚 Mga Kurso"):
    st.session_state.last_action = "kurso"
if col3.button("📋 Mga Kinakailangan"):
    st.session_state.last_action = "pangailangan"
if col4.button("📞 Makipag-ugnayan"):
    st.session_state.last_action = "kausapin"

# --------------------------
# Determine user input
# --------------------------
user_input = None

if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None

try:
    if user_input is None:
        chat_in = st.chat_input("I-type ang iyong mensahe dito...")
        if chat_in:
            user_input = chat_in
except Exception:
    if user_input is None:
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("I-type ang iyong mensahe dito:", value=st.session_state.typed_value, key="typed_value")
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("Ikaw", typed)):
            user_input = typed

# --------------------------
# Process input
# --------------------------
if user_input:
    st.session_state.messages.append(("Ikaw", user_input))
    with st.spinner("Nag-iisip si Bot..."):
        time.sleep(0.9)
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ Nagkaroon ng error: {e}"
    st.session_state.messages.append(("Bot", bot_reply))
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display conversation
# --------------------------
for role, msg in st.session_state.messages:
    if role == "Ikaw":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:15px; margin:5px; text-align:right;'>"
            f"🧑 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin:5px; text-align:left;'>"
            f"🤖 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
