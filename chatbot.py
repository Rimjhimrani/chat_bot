import streamlit as st
from difflib import get_close_matches

# --- 1. CONFIGURATION & Q&A DATA ---
st.set_page_config(page_title="FAQ Chatbot", page_icon="💬")

# Define your questions and answers here
FAQ_DATA = {
    "what is your name?": "I am the FAQ Assistant bot.",
    "how do i reset my password?": "To reset your password, click on 'Forgot Password' on the login page and follow the email instructions.",
    "what are your opening hours?": "We are open from 9 AM to 5 PM, Monday to Friday.",
    "where is your office located?": "Our headquarters are in San Francisco, California.",
    "how can i contact support?": "You can reach support via email at support@example.com or call 1-800-123-4567.",
    "hi": "Hello! How can I help you today?",
    "bye": "Goodbye! Feel free to return if you have more questions.",
}

# --- 2. HELPER FUNCTIONS ---
def find_best_match(user_query):
    """Finds the closest question from the FAQ keys."""
    questions = list(FAQ_DATA.keys())
    # Find the closest match with at least 60% similarity
    matches = get_close_matches(user_query.lower(), questions, n=1, cutoff=0.6)
    
    if matches:
        return FAQ_DATA[matches[0]]
    else:
        return "I'm sorry, I don't have information on that specific topic. Please try asking about our 'hours', 'location', or 'password reset'."

# --- 3. UI LAYOUT ---
st.title("💬 Company FAQ Bot")
st.info("Ask me questions about our services, hours, or support!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your automated assistant. How can I help you today?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Type your question here..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    response = find_best_match(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. SIDEBAR (Optional) ---
with st.sidebar:
    st.header("Helpful Commands")
    st.write("Try asking:")
    for q in list(FAQ_DATA.keys())[:4]: # Show first 4 questions
        st.write(f"- {q.capitalize()}")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
