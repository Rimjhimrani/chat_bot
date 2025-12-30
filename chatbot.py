import streamlit as st

# 1. Page Setup
st.set_page_config(page_title="Supply Chain Bot", page_icon="📦")
st.title("📦 Supply Chain Interactive Q&A")

# 2. Defined Question and Answer Data
SCM_DATA = {
    "Basics": {
        "What is SCM?": "Supply Chain Management (SCM) is the oversight of materials, information, and finances as they move from supplier to consumer.",
        "What is Lead Time?": "Lead time is the total time from when an order is placed until it is received by the customer.",
    },
    "Inventory": {
        "What is Safety Stock?": "Safety stock is extra inventory held as a buffer to prevent stockouts.",
        "What is JIT?": "Just-in-Time (JIT) is a strategy to receive goods only as they are needed in the production process.",
    }
}

# 3. Initialize Session State (This stores the chat history)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# 4. TOP SECTION: THE BUTTONS (The Options)
st.subheader("Step 1: Choose a Category")
cols = st.columns(len(SCM_DATA))
for i, category in enumerate(SCM_DATA.keys()):
    if cols[i].button(category):
        st.session_state.selected_category = category

# Step 2: Show Questions for that Category
if st.session_state.selected_category:
    st.write(f"---")
    st.subheader(f"Step 2: Questions about {st.session_state.selected_category}")
    
    questions = SCM_DATA[st.session_state.selected_category]
    for q_text, a_text in questions.items():
        # When this button is clicked, it updates the chat history
        if st.button(q_text):
            # Add User Question to History
            st.session_state.chat_history.append({"role": "user", "content": q_text})
            # Add Bot Answer to History
            st.session_state.chat_history.append({"role": "assistant", "content": a_text})

# 5. BOTTOM SECTION: THE CHAT DISPLAY
st.write("---")
st.subheader("Conversation")

# This loop displays everything currently in the chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 6. RESET BUTTON
if st.sidebar.button("Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.selected_category = None
    st.rerun()
