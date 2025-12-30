import streamlit as st

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="Supply Chain Expert", page_icon="📦")
st.title("📦 Supply Chain Knowledge Bot")
st.markdown("Select a topic below to see the answer in the chat.")

# --- 2. THE KNOWLEDGE BASE ---
# Questions are keys, Answers are values
SCM_FAQ = {
    "What is the Bullwhip Effect?": "The bullwhip effect is a supply chain phenomenon where small fluctuations in demand at the retail level cause progressively larger fluctuations at the wholesale, distributor, and manufacturer levels.",
    "Explain Just-in-Time (JIT)": "JIT is an inventory strategy where materials are ordered and received only as they are needed in the production process to reduce inventory holding costs and waste.",
    "What are the 5 main SCM KPIs?": "1. **OTIF (On-Time In-Full):** Delivery reliability.\n2. **Inventory Turnover:** How fast stock is sold.\n3. **Perfect Order Rate:** Orders with zero errors.\n4. **Cycle Time:** Total time from order to delivery.\n5. **Cash-to-Cash Cycle:** Time between paying suppliers and receiving customer payment.",
    "What is Supply Chain Resilience?": "Resilience is the ability of a supply chain to anticipate, adapt to, and recover from unexpected disruptions (like pandemics or natural disasters) while maintaining business continuity.",
    "Difference between 3PL and 4PL?": "3PL (Third-Party Logistics) focuses on the execution of transport and warehouse tasks. 4PL (Fourth-Party Logistics) acts as a strategic integrator that manages the entire supply chain, including other 3PLs.",
    "What is a Digital Twin in SCM?": "A Digital Twin is a virtual, real-time replica of the physical supply chain. It uses data to simulate 'what-if' scenarios, helping managers predict disruptions before they happen.",
    "What is Reverse Logistics?": "Reverse logistics is the process of moving goods from their final destination back to the seller or manufacturer for returns, repairs, recycling, or disposal.",
    "What is the EOQ (Economic Order Quantity)?": "EOQ is a formula used to find the optimal order size that minimizes the total costs of ordering and holding inventory."
}

# --- 3. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Supply Chain Assistant. Please choose a question from the sidebar or click a button below to begin."}
    ]

# Function to add to chat history
def handle_interaction(question):
    answer = SCM_FAQ[question]
    # Add user choice
    st.session_state.messages.append({"role": "user", "content": question})
    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- 4. OPTION SELECTION (Buttons) ---
# We put the options in a sidebar or a clean grid
with st.sidebar:
    st.header("Choose a Question")
    for q in SCM_FAQ.keys():
        if st.button(q, use_container_width=True):
            handle_interaction(q)
            st.rerun() # Refresh to show new messages instantly
    
    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- 5. DISPLAY CHAT ---
# We use st.container to keep the chat area organized
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Optional: Add a small footer
st.caption("Powered by Streamlit | Supply Chain Q&A v1.0")
