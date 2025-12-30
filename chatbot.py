import streamlit as st

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Supply Chain Guide", page_icon="📦")
st.title("📦 Supply Chain Assistant")
st.markdown("Click an option below to learn more, or type your own question.")

# --- 2. THE KNOWLEDGE BASE ---
# Structured as: Category -> Questions -> Answers
SCM_DATA = {
    "Basics 🏢": {
        "What is SCM?": "Supply Chain Management (SCM) is the oversight of materials, information, and finances as they move in a process from supplier to manufacturer to wholesaler to retailer to consumer.",
        "What is Lead Time?": "Lead time is the total time from when an order is placed until it is received by the customer.",
        "What is a Cold Chain?": "A cold chain is a temperature-controlled supply chain, essential for food and pharmaceuticals."
    },
    "Inventory 📉": {
        "What is Safety Stock?": "Safety stock is extra inventory held as a buffer to prevent stockouts caused by fluctuations in supply or demand.",
        "What is JIT?": "Just-in-Time (JIT) is an inventory strategy that aligns raw-material orders from suppliers directly with production schedules.",
        "What is EOQ?": "Economic Order Quantity (EOQ) is the ideal order quantity a company should purchase to minimize inventory costs."
    },
    "Logistics 🚛": {
        "What is 3PL?": "Third-Party Logistics (3PL) involves outsourcing distribution, warehousing, and fulfillment services to an external provider.",
        "What is Reverse Logistics?": "Reverse logistics is the process of moving goods from their final destination back to the manufacturer for returns or recycling.",
        "What is the Bullwhip Effect?": "The bullwhip effect happens when small changes in consumer demand cause large fluctuations in inventory levels up the chain."
    }
}

# --- 3. SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_category" not in st.session_state:
    st.session_state.current_category = None

# --- 4. HELPER FUNCTION TO ADD MESSAGES ---
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. SIDEBAR / RESET ---
with st.sidebar:
    if st.button("Reset Chat"):
        st.session_state.messages = []
        st.session_state.current_category = None
        st.rerun()

# --- 6. DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. THE OPTION MENU (The "Buttons" logic) ---
st.write("---")
st.write("### Choose a topic to explore:")

# Step 1: Show Main Categories
cols = st.columns(len(SCM_DATA))
for i, category in enumerate(SCM_DATA.keys()):
    if cols[i].button(category, use_container_width=True):
        st.session_state.current_category = category

# Step 2: Show specific questions for the selected category
if st.session_state.current_category:
    st.info(f"Questions about: {st.session_state.current_category}")
    questions = SCM_DATA[st.session_state.current_category]
    
    # Create buttons for each question
    for question, answer in questions.items():
        if st.button(f"❓ {question}"):
            # Add user selection to chat
            add_message("user", question)
            # Add bot response to chat
            add_message("assistant", answer)
            # Rerun to update chat history view
            st.rerun()

# --- 8. MANUAL TEXT INPUT (Optional) ---
if prompt := st.chat_input("Or type your question here..."):
    add_message("user", prompt)
    # Simple logic to check if it's in our data
    found = False
    for cat in SCM_DATA.values():
        if prompt in cat:
            add_message("assistant", cat[prompt])
            found = True
            break
    
    if not found:
        add_message("assistant", "I don't have a specific answer for that. Please use the menu buttons!")
    st.rerun()
