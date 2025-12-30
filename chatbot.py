import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="AI FAQ Bot", page_icon="🤖")
st.title("🤖 AI Chatbot")

# --- 2. DEFINE YOUR SPECIFIC ANSWERS (The "Fixed" part) ---
# The bot checks these first before asking the AI.
PREDEFINED_QA = {
    "what is your price?": "Our basic plan is $10/month, and Pro is $30/month.",
    "who is the ceo?": "The CEO of our company is Jane Doe.",
}

# --- 3. AI CONFIGURATION ---
# We use Streamlit Secrets to store the API Key securely
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Please set the GOOGLE_API_KEY in Streamlit Secrets.")
    st.stop()

# --- 4. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # STEP A: Check Predefined Answers first
    response_content = ""
    user_query = prompt.lower().strip()
    
    if user_query in PREDEFINED_QA:
        response_content = PREDEFINED_QA[user_query]
    else:
        # STEP B: If not predefined, use AI
        with st.spinner("Thinking..."):
            try:
                # We send the history so the AI has "memory"
                full_chat = model.start_chat(history=[])
                response = full_chat.send_message(prompt)
                response_content = response.text
            except Exception as e:
                response_content = "I'm having trouble connecting to my brain right now."

    # Display & Save Response
    with st.chat_message("assistant"):
        st.markdown(response_content)
    st.session_state.messages.append({"role": "assistant", "content": response_content})
