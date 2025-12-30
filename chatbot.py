import streamlit as st
import google.generativeai as genai
from difflib import get_close_matches

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="Supply Chain Expert Bot", page_icon="📦")
st.title("📦 Supply Chain Q&A Assistant")

# --- 2. DEFINED SUPPLY CHAIN KNOWLEDGE BASE ---
# These are the "fixed" answers your bot will prioritize.
SCM_KNOWLEDGE = {
    "what is supply chain management?": "SCM is the handling of the entire production flow of a good or service—starting from the raw components all the way to delivering the final product to the consumer.",
    "difference between logistics and scm?": "Logistics is a subset of SCM. Logistics focuses on the movement and storage of goods, while SCM covers the broader strategy, including sourcing, production, and supplier relationships.",
    "what is the bullwhip effect?": "The bullwhip effect is a supply chain phenomenon where small fluctuations in demand at the retail level cause progressively larger fluctuations at the wholesale, distributor, and manufacturer levels.",
    "what is just-in-time (jit)?": "JIT is an inventory strategy where materials are ordered and received only as they are needed in the production process to reduce inventory holding costs.",
    "what is 3pl?": "3PL stands for Third-Party Logistics. It refers to outsourcing e-commerce logistics processes, including inventory management, warehousing, and fulfillment to a third-party provider.",
    "what is reverse logistics?": "Reverse logistics is the process of moving goods from their final destination back to the seller or manufacturer for returns, repairs, or recycling.",
    "what is lead time?": "Lead time is the total amount of time that elapses between the placement of an order and the receipt of the goods.",
    "what is safety stock?": "Safety stock is extra inventory held as a buffer to mitigate the risk of stockouts caused by fluctuations in supply and demand.",
    "what is eoq?": "EOQ stands for Economic Order Quantity. It is a formula used to determine the optimal order quantity that minimizes total inventory costs (ordering and holding costs).",
    "what is a cold chain?": "A cold chain is a temperature-controlled supply chain used for perishable goods like food or pharmaceuticals to maintain quality and safety."
}

# --- 3. AI CONFIGURATION (For undefined questions) ---
# Ensure you have "GOOGLE_API_KEY" in your Streamlit Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    ai_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("AI features disabled: Please add GOOGLE_API_KEY to your Secrets.")

# --- 4. SESSION STATE (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your Supply Chain expert. Ask me about SCM concepts, logistics, or inventory!"}]

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. RESPONSE LOGIC ---
if prompt := st.chat_input("Ex: What is the bullwhip effect?"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # A. Search for a Match in defined knowledge
    query = prompt.lower().strip()
    matches = get_close_matches(query, SCM_KNOWLEDGE.keys(), n=1, cutoff=0.6)

    if matches:
        response = SCM_KNOWLEDGE[matches[0]]
    elif "GOOGLE_API_KEY" in st.secrets:
        # B. Fallback to AI if no match found
        with st.spinner("Consulting AI..."):
            try:
                ai_resp = ai_model.generate_content(f"You are a Supply Chain expert. Answer this: {prompt}")
                response = ai_resp.text
            except:
                response = "I'm sorry, I couldn't find a specific answer and my AI connection is offline."
    else:
        response = "I don't have a defined answer for that yet. Please ask about SCM basics!"

    # Show Assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
