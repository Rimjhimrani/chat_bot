import streamlit as st

# --- INITIAL CONFIGURATION ---
st.set_page_config(page_title="Agilomatrix Bot", layout="centered")

# Initialize Session State
if 'step' not in st.session_state:
    st.session_state.step = "industry_select"
if 'responses' not in st.session_state:
    st.session_state.responses = {}

def next_step(current_key, next_step_id):
    # Only progress if an answer is provided for text/radio
    if current_key in st.session_state.responses or "q" in current_key:
        st.session_state.step = next_step_id
        st.rerun()

def reset_survey():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.title("Agilomatrix ChatBot")

# --- LAYER 1: INDUSTRY ---
if st.session_state.step == "industry_select":
    st.subheader("Layer - 1")
    st.write("Which industry does your organization operate in?")
    choice = st.radio("Select one:", [
        "Manufacturing", "FMCG", "Retail & E-commerce", 
        "Logistics & 3PL", "Pharmaceuticals & Healthcare"
    ], index=None, key="industry_radio")
    
    if st.button("Next"):
        if choice:
            st.session_state.responses['Industry'] = choice
            st.session_state.step = "org_size"
            st.rerun()
        else:
            st.warning("Please select an option.")

# --- LAYER 2: ORGANIZATION SIZE ---
elif st.session_state.step == "org_size":
    st.subheader("Layer - 2")
    st.write("Q1. Select your organization size:")
    size = st.radio("By Employee Strength or Annual Turnover:", [
        "Micro (<50 employees / <₹50 Cr)",
        "Small (51-250 employees / ₹50-250 Cr)",
        "Medium (251-1,000 employees / ₹250-1,000 Cr)",
        "Large (1,001-5,000 employees / ₹1,000+ Cr)",
        "Enterprise (5,000+ employees)"
    ], index=None)
    
    if st.button("Next"):
        if size:
            st.session_state.responses['Org_Size'] = size
            st.session_state.step = f"{st.session_state.responses['Industry'].lower()}_q2"
            st.rerun()

# --- LAYER 3: INDUSTRY SPECIFIC BRANCHES ---

# --- MANUFACTURING BRANCH ---
elif st.session_state.step == "manufacturing_q2":
    val = st.text_input("Q2. Number of manufacturing plants")
    if st.button("Next"):
        st.session_state.responses['MFG_Q2'] = val
        st.session_state.step = "manufacturing_q3"
        st.rerun()

elif st.session_state.step == "manufacturing_q3":
    val = st.radio("Q3. Production model followed?", ["Make-to-Stock", "Make-to-Order", "Mixed"], index=None)
    if st.button("Next"):
        st.session_state.responses['MFG_Q3'] = val
        st.session_state.step = "manufacturing_q4"
        st.rerun()

elif st.session_state.step == "manufacturing_q4":
    st.write("Q4. What challenges are you currently facing?")
    opts = ["High inventory / stockouts", "Poor material flow", "Manual processes", "Low productivity", "Poor traceability", "High logistics cost", "Space constraints"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['MFG_Q4'] = selected
        st.session_state.step = "manufacturing_q5"
        st.rerun()

elif st.session_state.step == "manufacturing_q5":
    st.write("Q5. Which area needs improvement?")
    opts = ["Inventory management.", "Warehouse & line feeding.", "Logistics & transportation.", "Production planning.", "Supplier management.", "Visibility & traceability.", "Cost optimization"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['MFG_Q5'] = selected
        st.session_state.step = "contact_details"
        st.rerun()

# --- FMCG BRANCH ---
elif st.session_state.step == "fmcg_q2":
    val = st.radio("Q.2 Distribution model?", ["Direct", "Distributor", "Hybrid"], index=None)
    if st.button("Next"):
        st.session_state.responses['FMCG_Q2'] = val
        st.session_state.step = "fmcg_q3"
        st.rerun()

elif st.session_state.step == "fmcg_q3":
    st.write("Q.3 What challenges are you currently facing?")
    opts = ["Low forecast accuracy at SKU / channel level", "High inventory holding with frequent stock-outs", "Expiry and freshness management issues", "High distribution and secondary freight cost", "Inefficient replenishment to distributors / retailers", "Poor visibility of inventory across depots and channels", "Warehouse congestion during peak demand", "Packaging damage and handling losses", "Service level issues during promotions / seasonal peaks"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['FMCG_Q3'] = selected
        st.session_state.step = "fmcg_q4"
        st.rerun()

elif st.session_state.step == "fmcg_q4":
    st.write("Q4. Which areas of your FMCG supply chain need improvement?")
    opts = ["Demand forecasting & sales planning", "Inventory optimization & freshness management", "Production planning & scheduling", "Distributor & channel replenishment", "Warehouse operations & space utilization", "Packaging efficiency & damage reduction", "Transportation & secondary freight cost", "Service level (Fill rate / OTIF)", "Data visibility & reporting"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['FMCG_Q4'] = selected
        st.session_state.step = "contact_details"
        st.rerun()

# --- RETAIL BRANCH ---
elif st.session_state.step == "retail & e-commerce_q2":
    val = st.text_input("Q2. No of warehouses")
    if st.button("Next"):
        st.session_state.responses['Retail_Q2'] = val
        st.session_state.step = "retail_q3"
        st.rerun()

elif st.session_state.step == "retail_q3":
    val = st.radio("Q.3 Order fulfillment model?", ["Central DC", "Dark Store", "Store Fulfillment"], index=None)
    if st.button("Next"):
        st.session_state.responses['Retail_Q3'] = val
        st.session_state.step = "retail_q4"
        st.rerun()

elif st.session_state.step == "retail_q4":
    val = st.radio("Q.4 Warehouse automation level?", ["Manual", "Semi-auto", "Fully automated"], index=None)
    if st.button("Next"):
        st.session_state.responses['Retail_Q4'] = val
        st.session_state.step = "retail_q5a"
        st.rerun()

elif st.session_state.step == "retail_q5a":
    st.write("Q.5 Sales channels served?")
    opts = ["Online", "Offline", "Omnichannel"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Retail_Q5_Channels'] = selected
        st.session_state.step = "retail_q5b"
        st.rerun()

elif st.session_state.step == "retail_q5b":
    st.write("Q.5 What key challenges are you currently facing in your Retail & E-commerce operations?")
    opts = ["Frequent stock-outs or overselling", "Inaccurate inventory across channels", "SLA breaches in order delivery", "High fulfillment and last-mile delivery cost", "High returns / RTO impacting margins", "Slow order processing during peak demand", "Warehouse congestion and low productivity", "Packaging damage and customer complaints", "Limited end-to-end visibility", "Technology integration gaps (OMS / WMS / TMS)"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Retail_Q5_Challenges'] = selected
        st.session_state.step = "retail_q6"
        st.rerun()

elif st.session_state.step == "retail_q6":
    st.write("Q.6 Which areas of your Retail / E-commerce operations need improvement?")
    opts = ["Demand planning & forecasting", "Inventory planning & control", "Omnichannel inventory visibility", "Order management & orchestration", "Warehouse operations & fulfillment", "Picking, packing & dispatch processes", "Last-mile delivery operations", "Returns & reverse logistics", "Packaging & material handling", "Technology systems & integration", "Data analytics & performance reporting", "Cost optimization & productivity", "Customer experience enablement", "Scalability & peak-season readiness"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Retail_Q6'] = selected
        st.session_state.step = "contact_details"
        st.rerun()

# --- LOGISTICS BRANCH ---
elif st.session_state.step == "logistics & 3pl_q2":
    val = st.text_input("Q2 No of warehouses")
    if st.button("Next"):
        st.session_state.responses['Log_Q2'] = val
        st.session_state.step = "log_q3"
        st.rerun()

elif st.session_state.step == "log_q3":
    st.write("Q3 Service offerings?")
    selected = [opt for opt in ["Transportation", "Warehousing", "End-to-end SCM"] if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Log_Q3'] = selected
        st.session_state.step = "log_q4"
        st.rerun()

elif st.session_state.step == "log_q4":
    val = st.text_area("Q4 Industries and customer segments served?")
    if st.button("Next"):
        st.session_state.responses['Log_Q4'] = val
        st.session_state.step = "log_q5"
        st.rerun()

elif st.session_state.step == "log_q5":
    st.write("Q5 Geographic network coverage?")
    selected = [opt for opt in ["Domestic", "International"] if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Log_Q5'] = selected
        st.session_state.step = "log_q6"
        st.rerun()

elif st.session_state.step == "log_q6":
    val = st.radio("Q6 Pricing model used?", ["Fixed", "Variable", "Activity-based"], index=None)
    if st.button("Next"):
        st.session_state.responses['Log_Q6'] = val
        st.session_state.step = "log_q7"
        st.rerun()

elif st.session_state.step == "log_q7":
    st.write("Q7 What are the key operational challenges you are currently facing in your Logistics / 3PL operations?")
    opts = ["Low vehicle or warehouse utilization", "High transportation and operating costs", "On-time delivery (OTIF) performance issues", "Empty miles and poor route optimization", "Warehouse productivity and labor efficiency challenges", "Service level penalties and customer escalations", "Limited end-to-end visibility for customers", "Manual processes and system integration gaps", "Damage, loss, or claims management issues", "Capacity constraints during peak periods"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Log_Q7'] = selected
        st.session_state.step = "log_q8"
        st.rerun()

elif st.session_state.step == "log_q8":
    st.write("Q8 Which areas of your Logistics / 3PL operations need improvement?")
    opts = ["Transportation planning & execution", "Fleet management & utilization", "Route design & network planning", "Warehouse operations & fulfillment", "Labor planning & productivity management", "Order management & customer service", "Cost management & pricing models", "Technology platforms & system integration", "Data analytics & reporting", "Visibility & customer dashboards", "Quality, safety & compliance management", "Scalability & capacity planning", "Sustainability & ESG initiatives"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Log_Q8'] = selected
        st.session_state.step = "contact_details"
        st.rerun()

# --- PHARMA BRANCH ---
elif st.session_state.step == "pharmaceuticals & healthcare_q2":
    val = st.text_input("Q.2 Number of plants?")
    if st.button("Next"):
        st.session_state.responses['Pharma_Q2'] = val
        st.session_state.step = "pharma_q3"
        st.rerun()

elif st.session_state.step == "pharma_q3":
    st.write("Q3 Product category handled")
    selected = [opt for opt in ["Formulations", "API", "Medical devices"] if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Pharma_Q3'] = selected
        st.session_state.step = "pharma_q4"
        st.rerun()

elif st.session_state.step == "pharma_q4":
    val = st.radio("Q4 Temperature-controlled supply chain?", ["Yes", "Partial", "No"], index=None)
    if st.button("Next"):
        st.session_state.responses['Pharma_Q4'] = val
        st.session_state.step = "pharma_q5"
        st.rerun()

elif st.session_state.step == "pharma_q5":
    val = st.text_area("Q5 Temperature-controlled storage coverage?")
    if st.button("Next"):
        st.session_state.responses['Pharma_Q5'] = val
        st.session_state.step = "pharma_q6"
        st.rerun()

elif st.session_state.step == "pharma_q6":
    val = st.radio("Q6 Production model followed?", ["Make-to-Stock", "Make-to-Order", "Mixed"], index=None)
    if st.button("Next"):
        st.session_state.responses['Pharma_Q6'] = val
        st.session_state.step = "pharma_q7"
        st.rerun()

elif st.session_state.step == "pharma_q7":
    st.write("Q7 What are the key operational challenges you are currently facing in your pharmaceutical supply chain?")
    opts = ["Forecast inaccuracy and demand volatility", "Inventory build-up and expiry risk", "Batch release and regulatory lead-time delays", "Cold chain compliance and temperature excursions", "Limited end-to-end batch traceability", "Service level issues to distributors / institutions", "High logistics and distribution cost", "Manual processes impacting compliance", "Recall readiness and response challenges", "Limited real-time visibility across the supply chain"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Pharma_Q7'] = selected
        st.session_state.step = "pharma_q8"
        st.rerun()

elif st.session_state.step == "pharma_q8":
    st.write("Q8 Which areas of your pharmaceutical operations need improvement?")
    opts = ["Demand planning", "Inventory management", "Shelf-life & FEFO", "Batch & capacity planning", "Cold chain operations", "Distribution & logistics", "Quality & compliance", "Traceability & serialization", "Technology & data visibility", "Cost & productivity optimization"]
    selected = [opt for opt in opts if st.checkbox(opt)]
    if st.button("Next"):
        st.session_state.responses['Pharma_Q8'] = selected
        st.session_state.step = "contact_details"
        st.rerun()

# --- LAYER 4: CONTACT ---
elif st.session_state.step == "contact_details":
    st.subheader("Layer - 4")
    st.write("Please share your details")
    st.text_input("Name", key="user_name")
    st.text_input("Company", key="user_company")
    st.text_input("Email", key="user_email")
    st.text_input("Phone", key="user_phone")
    if st.button("Next"):
        st.session_state.step = "schedule"
        st.rerun()

elif st.session_state.step == "schedule":
    st.write("Schedule Meeting.")
    st.date_input("Date")
    st.time_input("Time")
    if st.button("Submit Survey"):
        st.success("Thank you! Your survey has been submitted.")
        st.balloons()
        st.write("### Your Responses Summary:")
        st.write(st.session_state.responses)
        if st.button("Start Over"):
            reset_survey()
