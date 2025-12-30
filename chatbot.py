import streamlit as st

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="SCM Interactive Guide", page_icon="📦", layout="centered")

# Custom CSS to make the chat look cleaner
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 Supply Chain Assistant")
st.markdown("Select a category, then click a question to see the answer.")

# --- 2. THE KNOWLEDGE BASE ---
SCM_DATA = {
    "Basics 🏢": {
        "What is SCM?": "Supply Chain Management (SCM) is the centralized management of the flow of goods and services, including all processes that transform raw materials into final products.",
        "What is Lead Time?": "Lead time is the latency between the initiation and completion of a process. In SCM, it's the time between placing an order and receiving it.",
        "What is a Cold Chain?": "A cold chain is a temperature-controlled supply chain. It is a series of refrigerated production, storage, and distribution activities.",
        "What is the Bullwhip Effect?": "It is a distribution channel phenomenon where demand fluctuations at the retail level increase progressively at the wholesale, distributor, and manufacturer levels."
    },
    "Inventory 📉": {
        "What is Safety Stock?": "Safety stock is an extra quantity of a product which is stored to prevent a stock-out situation caused by fluctuations in demand or supply.",
        "What is JIT?": "Just-in-Time (JIT) is an inventory management method where goods are received from suppliers only as they are needed, reducing inventory costs.",
        "What is EOQ?": "Economic Order Quantity (EOQ) is the ideal order quantity a company should purchase to minimize inventory costs such as holding costs and order costs.",
        "What is ABC Analysis?": "ABC analysis is an inventory categorization technique that divides items into three categories (A, B, and C) based on their importance and value."
    },
    "Logistics 🚛": {
        "What is 3PL vs 4PL?": "3PL (Third-Party Logistics) handles transportation and warehouse tasks. 4PL (Fourth-Party Logistics) manages the entire supply chain and acts as a single point of contact.",
        "What is Reverse Logistics?": "This involves the process of moving goods from their final destination back to the seller or manufacturer for returns, repairs, or recycling.",
        "What is Cross-Docking?": "Cross-docking is a logistics procedure where products from a supplier are distributed directly to a customer with little to no storage time.",
        "What is Last Mile Delivery?": "The 'Last Mile' is the final step of the delivery process when a parcel is moved from a transportation hub to its final destination (the customer)."
    }
}

# --- 3. SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Please select a category below to start learning about Supply Chain Management."}
    ]
if "current_category" not in st.session_state:
    st.session_state.current_category = None

# --- 4. DISPLAY CHAT HISTORY ---
# We display the chat at the top so it grows downwards
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. THE INTERACTIVE OPTIONS (The "Option Menu") ---
st.write("---")
st.subheader("Interactive Menu")

# Step 1: Category Selection
cat_cols = st.columns(len(SCM_DATA))
for i, category in enumerate(SCM_DATA.keys()):
    if cat_cols[i].button(category):
        st.session_state.current_category = category

# Step 2: Question Selection (Only shows if a category is picked)
if st.session_state.current_category:
    st.info(f"Showing questions for: **{st.session_state.current_category}**")
    questions = SCM_DATA[st.session_state.current_category]
    
    # Arrange questions in two columns for better look
    q_cols = st.columns(2)
    for i, (question, answer) in enumerate(questions.items()):
        col_idx = i % 2
        if q_cols[col_idx].button(f"🔎 {question}"):
            # When clicked, add both Question and Answer to history
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": answer})
            # Rerun to update the chat display above
            st.rerun()

# --- 6. MANUAL SEARCH (Optional) ---
st.write("---")
if prompt := st.chat_input("Or type a specific question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Basic search logic
    found_answer = "I'm sorry, I don't have a specific answer for that in my database. Please try using the buttons above!"
    for cat in SCM_DATA.values():
        for q, a in cat.items():
            if prompt.lower() in q.lower():
                found_answer = a
                break
    
    st.session_state.messages.append({"role": "assistant", "content": found_answer})
    st.rerun()

# --- 7. RESET BUTTON ---
with st.sidebar:
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.current_category = None
        st.rerun()
