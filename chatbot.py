import streamlit as st
from openai import OpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="Supply Chain Survey Bot", layout="centered")
st.title("📋 Industry Survey Assistant")

# --- FULL DATA EXTRACTION FROM YOUR SCREENSHOT ---
SURVEY_DATA = {
    "Layer_1": {
        "question": "Which industry does your organization operate in?",
        "options": ["Manufacturing", "FMCG", "Retail & E-commerce", "Logistics & 3PL", "Pharmaceuticals & Healthcare"]
    },
    "Layer_2": {
        "question": "Q1. Select your organization size:",
        "sub_questions": [
            "By Employee Strength: Micro (<50), Small (51-250), Medium (251-1,000), Large (1,001-5,000), Enterprise (5,000+)",
            "OR By Annual Turnover: <₹50 Cr, ₹50-250 Cr, ₹1,000+ Cr"
        ]
    },
    "Industry_Specific": {
        "Manufacturing": [
            "Q2. Number of manufacturing plants?",
            "Q3. Production model followed? (Make-to-Stock, Make-to-Order, Mixed)",
            "Q4. What challenges are you currently facing? (Options: High inventory/stockouts, Poor material flow, Manual processes, Low productivity, Poor traceability, High logistics cost, Space constraints)",
            "Q5. Which area needs improvement? (Options: Inventory management, Warehouse & line feeding, Logistics & transportation, Production planning, Supplier management, Visibility & traceability, Cost optimization)"
        ],
        "FMCG": [
            "Q2. Distribution model? (Direct, Distributor, Hybrid)",
            "Q3. What challenges are you currently facing? (Options: Low forecast accuracy, High inventory holding, Expiry/freshness issues, High distribution cost, Inefficient replenishment, Poor visibility, Warehouse congestion, Packaging damage, Service level issues)",
            "Q4. Which areas of your FMCG supply chain need improvement? (Options: Demand forecasting, Inventory optimization, Production planning, Distributor replenishment, Warehouse operations, Packaging efficiency, Transportation cost, Service level (Fill rate/OTIF), Data visibility)"
        ],
        "Retail & E-commerce": [
            "Q2. No of warehouses?",
            "Q3. Order fulfillment model? (Central DC, Dark Store, Store Fulfillment)",
            "Q4. Warehouse automation level? (Manual, Semi-auto, Fully automated)",
            "Q5. Sales channels served? (Online, Offline, Omnichannel) AND what key challenges? (Stock-outs, Inventory accuracy, SLA breaches, High delivery cost, High returns/RTO, Slow processing, Congestion, Packaging damage, Limited visibility, Tech gaps)",
            "Q6. Which areas of operations need improvement? (Demand planning, Inventory control, Omnichannel visibility, Order orchestration, Warehouse ops, Picking/dispatch, Last-mile, Returns, Packaging, Tech systems, Analytics, Cost optimization, Customer experience, Scalability)"
        ],
        "Logistics & 3PL": [
            "Q2. No of warehouses?",
            "Q3. Service offerings? (Transportation, Warehousing, End-to-end SCM)",
            "Q4. Industries and customer segments served?",
            "Q5. Geographic network coverage? (Domestic, International)",
            "Q6. Pricing model used? (Fixed, Variable, Activity-based)",
            "Q7. Key operational challenges? (Utilization, High operating costs, OTIF performance, Empty miles, Labor efficiency, Penalties, Visibility, System integration, Damage/Claims, Capacity constraints)",
            "Q8. Which areas need improvement? (Transport planning, Fleet management, Route design, Warehouse ops, Labor planning, Order management, Cost management, Tech platforms, Data analytics, Visibility dashboards, Quality/Compliance, Scalability, Sustainability)"
        ],
        "Pharmaceuticals & Healthcare": [
            "Q2. Number of plants?",
            "Q3. Product category handled? (Formulations, API, Medical devices)",
            "Q4. Temperature-controlled supply chain? (Yes, Partial, No)",
            "Q5. Temperature-controlled storage coverage?",
            "Q6. Production model followed? (Make-to-Stock, Make-to-Order, Mixed)",
            "Q7. Key operational challenges? (Forecast inaccuracy, Expiry risk, Batch release delays, Cold chain compliance, Traceability, High distribution cost, Manual processes, Recall readiness, Real-time visibility)",
            "Q8. Which areas need improvement? (Demand planning, Inventory management, Shelf-life & FEFO, Batch planning, Cold chain ops, Distribution, Quality/Compliance, Traceability, Tech/Data visibility, Cost optimization)"
        ]
    },
    "Layer_4": "Q. Final Details: Please provide your Name, Company, Email, Phone and a preferred Date/Time for a schedule meeting."
}

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": f"Hello! Let's get started. {SURVEY_DATA['Layer_1']['question']} \n\nOptions: {', '.join(SURVEY_DATA['Layer_1']['options'])}"}]
if "industry" not in st.session_state:
    st.session_state.industry = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    if not api_key:
        st.info("Enter your OpenAI API key to interact with the bot.")
    st.divider()
    if st.button("Clear Chat"):
        st.session_state.messages = [{"role": "assistant", "content": f"Hello! Let's get started. {SURVEY_DATA['Layer_1']['question']}"}]
        st.session_state.industry = None
        st.rerun()

# --- CHAT ENGINE ---
client = OpenAI(api_key=api_key) if api_key else None

def get_ai_response():
    system_prompt = f"""
    You are an expert Supply Chain Consultant. Your job is to conduct a survey based EXACTLY on this data structure: {SURVEY_DATA}.
    
    RULES:
    1. Ask ONLY ONE question at a time.
    2. Follow the sequence: Layer 1 -> Layer 2 -> Layer 3 (Specific to the chosen industry) -> Layer 4.
    3. If the user mentions one of the industries ({SURVEY_DATA['Layer_1']['options']}), remember it and use it to ask the correct Q2, Q3, etc. from 'Industry_Specific'.
    4. Be professional but brief.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
    )
    return response.choices[0].message.content

# --- UI LOGIC ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not api_key:
        st.error("Please provide an API Key in the sidebar.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Logic to "lock in" the industry choice
        for ind in SURVEY_DATA["Layer_1"]["options"]:
            if ind.lower() in prompt.lower():
                st.session_state.industry = ind

        with st.chat_message("assistant"):
            response = get_ai_response()
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
