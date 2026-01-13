import streamlit as st
import pandas as pd

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Supply Chain Survey", layout="wide")

# Initialize Session State to track progress and data
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'survey_data' not in st.session_state:
    st.session_state.survey_data = {}

def reset_survey():
    st.session_state.step = 1
    st.session_state.survey_data = {}
    st.rerun()

st.title("Supply Chain Organization Survey")
st.info("Please fill out the details based on your organization's operations.")

# --- LAYER 1: INDUSTRY SELECTION ---
if st.session_state.step == 1:
    st.header("Layer - 1: Industry")
    industry = st.selectbox(
        "Which industry does your organization operate in?",
        ["Select Industry", "Manufacturing", "FMCG", "Retail & E-commerce", "Logistics & 3PL", "Pharmaceuticals & Healthcare"],
        index=0
    )
    if industry != "Select Industry":
        st.session_state.survey_data['Industry'] = industry
        if st.button("Next"):
            st.session_state.step = 2
            st.rerun()

# --- LAYER 2: ORGANIZATION SIZE ---
elif st.session_state.step == 2:
    st.header("Layer - 2: Organization Size")
    st.subheader("Q1. Select your organization size:")
    
    size_option = st.radio(
        "By Employee Strength OR By Annual Turnover",
        [
            "Micro (<50 employees / <₹50 Cr)",
            "Small (51–250 employees / ₹50-250 Cr)",
            "Medium (251–1,000 employees / ₹250-1,000 Cr)",
            "Large (1,001–5,000 employees / ₹1,000+ Cr)",
            "Enterprise (5,000+ employees)"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.survey_data['Org Size'] = size_option
            st.session_state.step = 3
            st.rerun()

# --- LAYER 3: INDUSTRY SPECIFIC QUESTIONS ---
elif st.session_state.step == 3:
    industry = st.session_state.survey_data['Industry']
    st.header(f"Layer - 3: {industry} Details")

    # --- 1. MANUFACTURING ---
    if industry == "Manufacturing":
        q2 = st.text_input("Q.2 Number of manufacturing plants")
        q3 = st.radio("Q3 Production model followed?", ["Make-to-Stock", "Make-to-Order", "Mixed"])
        q4 = st.multiselect("Q4 What challenges are you currently facing?", 
                           ["High inventory / stockouts", "Poor material flow", "Manual processes", "Low productivity", "Poor traceability", "High logistics cost", "Space constraints"])
        q5 = st.multiselect("Q5 Which area needs improvement?", 
                           ["Inventory management", "Warehouse & line feeding", "Logistics & transportation.", "Production planning.", "Supplier management.", "Visibility & traceability.", "Cost optimization"])
        
        st.session_state.survey_data.update({"Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5})

    # --- 2. FMCG ---
    elif industry == "FMCG":
        q2 = st.radio("Q.2 Distribution model?", ["Direct", "Distributor", "Hybrid"])
        q3 = st.multiselect("Q.3 What challenges are you currently facing?", 
                           ["Low forecast accuracy at SKU / channel level", "High inventory holding with frequent stock-outs", "Expiry and freshness management issues", "High distribution and secondary freight cost", "Inefficient replenishment to distributors / retailers", "Poor visibility of inventory across depots and channels", "Warehouse congestion during peak demand", "Packaging damage and handling losses", "Service level issues during promotions / seasonal peaks"])
        q4 = st.multiselect("Q4 Which areas of your FMCG supply chain need improvement?", 
                           ["Demand forecasting & sales planning", "Inventory optimization & freshness management", "Production planning & scheduling", "Distributor & channel replenishment", "Warehouse operations & space utilization", "Packaging efficiency & damage reduction", "Transportation & secondary freight cost", "Service level (Fill rate / OTIF)", "Data visibility & reporting"])
        
        st.session_state.survey_data.update({"Q2": q2, "Q3": q3, "Q4": q4})

    # --- 3. RETAIL & E-COMMERCE ---
    elif industry == "Retail & E-commerce":
        q2 = st.text_input("Q2. No of warehouses")
        q3 = st.radio("Q.3 Order fulfillment model?", ["Central DC", "Dark Store", "Store Fulfillment"])
        q4 = st.radio("Q.4 Warehouse automation level?", ["Manual", "Semi-auto", "Fully automated"])
        q5_1 = st.multiselect("Q.5 Sales channels served?", ["Online", "Offline", "Omnichannel"])
        q5_2 = st.multiselect("Q.5 What key challenges are you currently facing in your Retail & E-commerce operations?", 
                             ["Frequent stock-outs or overselling", "Inaccurate inventory across channels", "SLA breaches in order delivery", "High fulfillment and last-mile delivery cost", "High returns / RTO impacting margins", "Slow order processing during peak demand", "Warehouse congestion and low productivity", "Packaging damage and customer complaints", "Limited end-to-end visibility", "Technology integration gaps (OMS / WMS / TMS)"])
        q6 = st.multiselect("Q.6 Which areas of your Retail / E-commerce operations need improvement?", 
                           ["Demand planning & forecasting", "Inventory planning & control", "Omnichannel inventory visibility", "Order management & orchestration", "Warehouse operations & fulfillment", "Picking, packing & dispatch processes", "Last-mile delivery operations", "Returns & reverse logistics", "Packaging & material handling", "Technology systems & integration (OMS / WMS / TMS)", "Data analytics & performance reporting", "Cost optimization & productivity", "Customer experience enablement", "Scalability & peak-season readiness"])
        
        st.session_state.survey_data.update({"Q2": q2, "Q3": q3, "Q4": q4, "Q5_Channels": q5_1, "Q5_Challenges": q5_2, "Q6": q6})

    # --- 4. LOGISTICS & 3PL ---
    elif industry == "Logistics & 3PL":
        q2 = st.text_input("Q2 No of warehouses")
        q3 = st.multiselect("Q3 Service offerings?", ["Transportation", "Warehousing", "End-to-end SCM"])
        q4 = st.text_area("Q4 Industries and customer segments served?")
        q5 = st.multiselect("Q5 Geographic network coverage?", ["Domestic", "International"])
        q6 = st.radio("Q6 Pricing model used?", ["Fixed", "Variable", "Activity-based"])
        q7 = st.multiselect("Q7 What are the key operational challenges you are currently facing in your Logistics / 3PL operations?", 
                           ["Low vehicle or warehouse utilization", "High transportation and operating costs", "On-time delivery (OTIF) performance issues", "Empty miles and poor route optimization", "Warehouse productivity and labor efficiency challenges", "Service level penalties and customer escalations", "Limited end-to-end visibility for customers", "Manual processes and system integration gaps", "Damage, loss, or claims management issues", "Capacity constraints during peak periods"])
        q8 = st.multiselect("Q8 Which areas of your Logistics / 3PL operations need improvement?", 
                           ["Transportation planning & execution", "Fleet management & utilization", "Route design & network planning", "Warehouse operations & fulfillment", "Labor planning & productivity management", "Order management & customer service", "Cost management & pricing models", "Technology platforms & system integration", "Data analytics & reporting", "Visibility & customer dashboards", "Quality, safety & compliance management", "Scalability & capacity planning", "Sustainability & ESG initiatives"])
        
        st.session_state.survey_data.update({"Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7, "Q8": q8})

    # --- 5. PHARMACEUTICALS & HEALTHCARE ---
    elif industry == "Pharmaceuticals & Healthcare":
        q2 = st.text_input("Q.2 Number of plants?")
        q3 = st.multiselect("Q3 Product category handled", ["Formulations", "API", "Medical devices"])
        q4 = st.radio("Q4 Temperature-controlled supply chain?", ["Yes", "Partial", "No"])
        q5 = st.text_area("Q5 Temperature-controlled storage coverage?")
        q6 = st.radio("Q6 Production model followed?", ["Make-to-Stock", "Make-to-Order", "Mixed"])
        q7 = st.multiselect("Q7 What are the key operational challenges you are currently facing in your pharmaceutical supply chain?", 
                           ["Forecast inaccuracy and demand volatility", "Inventory build-up and expiry risk", "Batch release and regulatory lead-time delays", "Cold chain compliance and temperature excursions", "Limited end-to-end batch traceability", "Service level issues to distributors / institutions", "High logistics and distribution cost", "Manual processes impacting compliance", "Recall readiness and response challenges", "Limited real-time visibility across the supply chain"])
        q8 = st.multiselect("Q8 Which areas of your pharmaceutical operations need improvement?", 
                           ["Demand planning", "Inventory management", "Shelf-life & FEFO", "Batch & capacity planning", "Cold chain operations", "Distribution & logistics", "Quality & compliance", "Traceability & serialization", "Technology & data visibility", "Cost & productivity optimization"])
        
        st.session_state.survey_data.update({"Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7, "Q8": q8})

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state.step = 4
            st.rerun()

# --- LAYER 4: CONTACT & SCHEDULING ---
elif st.session_state.step == 4:
    st.header("Layer - 4: Final Details")
    st.write("Please share your details")
    
    col_a, col_b = st.columns(2)
    with col_a:
        name = st.text_input("Name")
        company = st.text_input("Company")
    with col_b:
        email = st.text_input("Email")
        phone = st.text_input("Phone")
    
    st.markdown("---")
    st.subheader("Schedule Meeting")
    date = st.date_input("Date")
    time = st.time_input("Time")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Submit Survey"):
            st.session_state.survey_data.update({
                "Contact_Name": name, "Contact_Company": company,
                "Contact_Email": email, "Contact_Phone": phone,
                "Meeting_Date": str(date), "Meeting_Time": str(time)
            })
            st.session_state.step = 5
            st.rerun()

# --- FINAL SUMMARY ---
elif st.session_state.step == 5:
    st.success("Thank you! Your survey has been submitted successfully.")
    st.subheader("Summary of your responses:")
    st.json(st.session_state.survey_data)
    
    if st.button("Restart Survey"):
        reset_survey()
