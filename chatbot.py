import streamlit as st
from openai import OpenAI

# --- INITIAL CONFIGURATION ---
st.set_page_config(page_title="Supply Chain Survey Bot", layout="centered")
st.title("🚢 Supply Chain Consultation Bot")

# --- DATA STRUCTURE (Extracted from your flowchart) ---
SURVEY_FLOW = {
    "step_1": {
        "question": "Which industry does your organization operate in?",
        "options": ["Manufacturing", "FMCG", "Retail & E-commerce", "Logistics & 3PL", "Pharmaceuticals & Healthcare"],
        "type": "radio"
    },
    "step_2": {
        "question": "Select your organization size (By Employee Strength or Annual Turnover):",
        "options": [
            "Micro (<50 employees / <₹50 Cr)", 
            "Small (51-250 employees / ₹50-250 Cr)", 
            "Medium (251-1,000 employees / ₹250-1,000 Cr)", 
            "Large (1,001-5,000 employees / ₹1,000+ Cr)", 
            "Enterprise (5,000+ employees)"
        ],
        "type": "radio"
    },
    "industry_specific": {
        "Manufacturing": [
            {"q": "Q2. Number of manufacturing plants?", "type": "radio", "options": ["1-2", "3-5", "5-10", "10+"]},
            {"q": "Q3. Production model followed?", "type": "radio", "options": ["Make-to-Stock", "Make-to-Order", "Mixed"]},
            {"q": "Q4. What challenges are you currently facing? (Select all that apply)", "type": "multiselect", 
             "options": ["High inventory/stockouts", "Poor material flow", "Manual processes", "Low productivity", "Poor traceability", "High logistics cost", "Space constraints"]},
            {"q": "Q5. Which area needs improvement?", "type": "multiselect", 
             "options": ["Inventory management", "Warehouse & line feeding", "Logistics & transportation", "Production planning", "Supplier management", "Visibility & traceability", "Cost optimization"]}
        ],
        "FMCG": [
            {"q": "Q2. Distribution model?", "type": "radio", "options": ["Direct", "Distributor", "Hybrid"]},
            {"q": "Q3. Current challenges?", "type": "multiselect", "options": ["Low forecast accuracy", "High inventory holding", "Expiry issues", "High distribution cost", "Warehouse congestion", "Packaging damage"]},
            {"q": "Q4. Improvement areas?", "type": "multiselect", "options": ["Demand forecasting", "Inventory optimization", "Production planning", "Packaging efficiency", "Data visibility"]}
        ],
        # (Add other industries here following the same pattern)
    },
    "final": {"q": "Please enter your contact details (Name, Company, Email, Phone):", "type": "text"}
}

# --- INITIALIZE SESSION STATE ---
if "step" not in st.session_state:
    st.session_state.step = "step_1"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "industry_step_index" not in st.session_state:
    st.session_state.industry_step_index = 0

# --- SIDEBAR FOR API KEY ---
with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password")
    if st.button("Reset Survey"):
        st.session_state.clear()
        st.rerun()

# --- HELPER: ADVANCE SURVEY ---
def handle_selection(val, key_name):
    st.session_state.user_data[key_name] = val
    st.session_state.chat_history.append({"role": "user", "content": str(val)})
    
    # Logic to move to next step
    if st.session_state.step == "step_1":
        st.session_state.step = "step_2"
    elif st.session_state.step == "step_2":
        st.session_state.step = "industry_branch"
    elif st.session_state.step == "industry_branch":
        industry = st.session_state.user_data["step_1"]
        if st.session_state.industry_step_index < len(SURVEY_FLOW["industry_specific"].get(industry, [])) - 1:
            st.session_state.industry_step_index += 1
        else:
            st.session_state.step = "final"
    st.rerun()

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- CURRENT QUESTION UI (Ticking Options) ---
with st.chat_message("assistant"):
    if st.session_state.step == "step_1":
        q = SURVEY_FLOW["step_1"]
        st.write(q["question"])
        choice = st.radio("Choose one:", q["options"], key="s1", index=None)
        if choice:
            handle_selection(choice, "step_1")

    elif st.session_state.step == "step_2":
        q = SURVEY_FLOW["step_2"]
        st.write(q["question"])
        choice = st.radio("Choose one:", q["options"], key="s2", index=None)
        if choice:
            handle_selection(choice, "step_2")

    elif st.session_state.step == "industry_branch":
        industry = st.session_state.user_data["step_1"]
        questions = SURVEY_FLOW["industry_specific"].get(industry, [{"q": "No data for this industry yet.", "type": "radio", "options": ["Continue"]}])
        curr_q = questions[st.session_state.industry_step_index]
        
        st.write(curr_q["q"])
        if curr_q["type"] == "radio":
            choice = st.radio("Select one:", curr_q["options"], key=f"ind_{st.session_state.industry_step_index}", index=None)
            if choice:
                handle_selection(choice, f"industry_q_{st.session_state.industry_step_index}")
        elif curr_q["type"] == "multiselect":
            choices = st.multiselect("Select all that apply:", curr_q["options"], key=f"ind_m_{st.session_state.industry_step_index}")
            if st.button("Confirm Selection"):
                handle_selection(choices, f"industry_q_{st.session_state.industry_step_index}")

    elif st.session_state.step == "final":
        st.write(SURVEY_FLOW["final"]["q"])
        contact = st.text_area("Type your details here...")
        if st.button("Submit Survey"):
            st.session_state.user_data["contact"] = contact
            st.success("Thank you! Our team will contact you soon.")
            # Optional: Use OpenAI to summarize and say goodbye
            if api_key:
                client = OpenAI(api_key=api_key)
                summary = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": f"The user completed the survey with these details: {st.session_state.user_data}. Write a warm goodbye."}]
                )
                st.write(summary.choices[0].message.content)
