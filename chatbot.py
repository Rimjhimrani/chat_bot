import streamlit as st

# --- 1. CONFIG & SETTINGS ---
st.set_page_config(page_title="Global SCM Expert", page_icon="🌐", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f0f2f6; border: 1px solid #d1d5db; }
    .stButton>button:hover { background-color: #e5e7eb; border-color: #3b82f6; }
    .stInfo { background-color: #eff6ff; border-left-color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE EXPANDED KNOWLEDGE BASE ---
SCM_DATA = {
    "Fundamentals & Strategy 🏢": {
        "What is SCM?": "Supply Chain Management is the handling of the entire production flow of a good—from raw materials to delivering the final product to the consumer.",
        "SCM vs Logistics?": "Logistics is a subset of SCM. Logistics focuses on movement and storage, while SCM covers sourcing, production, and strategy.",
        "What is the Bullwhip Effect?": "A phenomenon where small fluctuations in demand at the retail level cause larger fluctuations at the wholesale and manufacturer levels.",
        "What is Lead Time?": "The total time from placing an order until it is received. Reducing lead time is a key goal in supply chain optimization.",
        "What is Vertical Integration?": "When a company owns multiple stages of its supply chain (e.g., a car maker owning a tire factory) to control costs and quality.",
        "Define Supply Chain Resilience": "The ability of a supply chain to adapt to and recover from disruptions (like pandemics or disasters) while maintaining continuity."
    },
    "Inventory & Planning 📉": {
        "What is Safety Stock?": "Extra inventory held as a buffer to prevent stockouts caused by unexpected demand spikes or supply delays.",
        "Explain JIT (Just-in-Time)": "A 'pull' system where materials are ordered only as needed for production, reducing waste and holding costs.",
        "What is EOQ?": "Economic Order Quantity—the ideal order size that minimizes both ordering and holding costs.",
        "What is ABC Analysis?": "Categorizing inventory: A (high value, low volume), B (moderate), and C (low value, high volume) to focus management efforts.",
        "What is Demand Forecasting?": "Using historical data and trends to predict future customer demand to plan production and inventory.",
        "What is VMI (Vendor Managed Inventory)?": "A system where the supplier monitors the buyer’s inventory and automatically replenishes it as needed."
    },
    "Logistics & Distribution 🚛": {
        "3PL vs 4PL?": "3PL handles logistics tasks (shipping/warehousing). 4PL manages the entire supply chain, including other 3PL providers.",
        "What is Reverse Logistics?": "The process of moving goods from the customer back to the seller for returns, repairs, or recycling.",
        "Define Cross-Docking": "Unloading goods from an incoming vehicle and loading them directly into outbound vehicles with zero storage time.",
        "What is Last Mile Delivery?": "The final step of the delivery process from a distribution hub to the customer's doorstep—often the most expensive part.",
        "Explain Cold Chain": "A temperature-controlled supply chain used for perishable goods like vaccines or fresh food.",
        "What is Intermodal Transport?": "Using two or more modes of transport (e.g., ship and truck) to move goods without handling the freight itself."
    },
    "Procurement & Sourcing 🤝": {
        "What is Strategic Sourcing?": "A procurement process that continuously improves and re-evaluates purchasing activities to find the best value.",
        "Procurement vs Purchasing?": "Purchasing is the transactional act of buying. Procurement is the strategic process of sourcing, negotiating, and relationship management.",
        "What is an RFP?": "Request for Proposal—a document used to solicit bids from potential suppliers for a specific project or service.",
        "Define TCO (Total Cost of Ownership)": "The total cost of an asset over its life, including purchase price, shipping, storage, maintenance, and disposal.",
        "Explain Dual Sourcing": "Using two different suppliers for the same component to reduce risk if one supplier fails.",
        "What are Procurement KPIs?": "Metrics like cost savings, supplier quality, delivery performance, and contract compliance."
    },
    "Tech & Sustainability 🤖": {
        "What is a Digital Twin?": "A virtual replica of the physical supply chain used to simulate scenarios and predict disruptions.",
        "Blockchain in SCM?": "Used for 'Traceability'—creating an unchangeable record of every transaction or movement of a product.",
        "IoT in Warehousing?": "Sensors and connected devices that track inventory location, temperature, and shelf life in real-time.",
        "What is Green Supply Chain?": "Integrating environmentally friendly practices into all stages of SCM, from product design to logistics.",
        "Define Circular Supply Chain": "A model where products are returned, refurbished, and put back into the supply chain to minimize waste.",
        "Role of AI in SCM?": "Used for automated demand forecasting, route optimization, and predictive maintenance of delivery fleets."
    }
}

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am your **Global Supply Chain Expert**. Choose a category to start your learning journey."}]
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

# --- 4. DISPLAY CHAT HISTORY ---
st.write("### 💬 Expert Conversation")
chat_placeholder = st.container(height=400, border=True)
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 5. THE OPTION MENU ---
st.write("---")
st.subheader("🛠️ Control Panel")

# Step 1: Choose Category
st.write("**Step 1: Choose a Topic Category**")
cat_cols = st.columns(len(SCM_DATA))
for i, category in enumerate(SCM_DATA.keys()):
    if cat_cols[i].button(category):
        st.session_state.selected_category = category

# Step 2: Choose Question
if st.session_state.selected_category:
    st.write(f"**Step 2: Choose a question about {st.session_state.selected_category}**")
    questions = SCM_DATA[st.session_state.selected_category]
    
    # Show questions in a grid (3 per row)
    q_cols = st.columns(3)
    for idx, (question, answer) in enumerate(questions.items()):
        col_idx = idx % 3
        if q_cols[col_idx].button(f"❓ {question}", key=f"q_{idx}"):
            # Update Chat History
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()

# --- 6. SIDEBAR TOOLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=100)
    st.title("Admin Panel")
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat reset. How can I help you today?"}]
        st.session_state.selected_category = None
        st.rerun()
    st.write("---")
    st.info("This bot uses a predefined knowledge base. You can expand it by adding more items to the `SCM_DATA` dictionary in the code.")
