import streamlit as st
import google.generativeai as genai
from difflib import get_close_matches

# --- 1. CONFIG & API SETUP ---
st.set_page_config(page_title="SCM AI Assistant", page_icon="🤖")

# Securely fetch API Key from Streamlit Secrets (for deployment)
# For local testing, you can replace this with: API_KEY = "YOUR_KEY_HERE"
API_KEY = st.secrets.get("GOOGLE_API_KEY", "")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing Google API Key! Please add it to your Streamlit Secrets.")

# --- 2. YOUR DEFINED QUESTIONS (Knowledge Base) ---
SCM_DEFINED = {
    "What is your price?": "Our standard supply chain consulting starts at $500/month.",
    "Who is the CEO?": "Our CEO is Sarah Jenkins, an expert in global logistics.",
    "Where are you located?": "Our main hub is in Singapore, with offices in London and New York.",
    "Do you offer 24/7 support?": "Yes, our platinum members get 24/7 priority support."
}

# --- 3. SESSION STATE (Chat Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Supply Chain expert. Ask me anything or choose an option below."}
    ]

# --- 4. UI: SIDEBAR OPTIONS ---
with st.sidebar:
    st.title("Admin Panel")
    st.info("The bot checks defined answers first, then uses AI.")
    
    st.subheader("Quick Options")
    for q in SCM_DEFINED.keys():
        if st.button(q):
            # Simulate user typing this question
            user_prompt = q
            st.session_state.messages.append({"role": "user", "content": q})
            st.session_state.messages.append({"role": "assistant", "content": SCM_DEFINED[q]})
            st.rerun()

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- 5. MAIN CHAT INTERFACE ---
st.title("🤖 Supply Chain AI Bot")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("Ask about Bullwhip effect, JIT, or our services..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- HYBRID LOGIC ---
    # A. Check for Defined Questions (Fuzzy Match)
    matches = get_close_matches(prompt.lower(), [k.lower() for k in SCM_DEFINED.keys()], n=1, cutoff=0.7)
    
    if matches:
        # Find the original key to get the correct answer
        original_key = [k for k in SCM_DEFINED.keys() if k.lower() == matches[0]][0]
        response = SCM_DEFINED[original_key]
    else:
        # B. Fallback to AI (Gemini)
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                try:
                    # Provide context to the AI so it stays in "Expert" mode
                    ai_prompt = f"You are a professional Supply Chain Expert. Answer this question concisely: {prompt}"
                    ai_response = model.generate_content(ai_prompt)
                    response = ai_response.text
                    st.markdown(response)
                except Exception as e:
                    response = "I'm having trouble connecting to my AI brain. Please try again."
                    st.write(response)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
