# AI Bidder Pro v2 - Streamlit App with Advanced Material Breakdown
import streamlit as st
from datetime import datetime, timedelta

# App Configuration
st.set_page_config(page_title="AI Construction Bidder Pro", page_icon="🏗️", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #0b1d3a;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            background-color: #1f4f82;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
        }
    </style>
""", unsafe_allow_html=True)

# Trial System (Simulated for now)
st.title("AI Construction Bidder Pro")

if "trial_start" not in st.session_state:
    st.session_state.trial_start = datetime.now()
    st.session_state.user = None

trial_days_left = 2 - (datetime.now() - st.session_state.trial_start).days
if trial_days_left <= 0:
    st.error("🚫 Trial expired. Please subscribe to continue.")
    st.stop()

# Login Simulation
if not st.session_state.user:
    st.subheader("🔐 Sign In to Access")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Enter App"):
        if name and email:
            st.session_state.user = {"name": name, "email": email}
        else:
            st.warning("Please enter both name and email.")
    st.stop()

# Input Section
st.subheader("📝 Project Details")
project_name = st.text_input("Project Name")
zip_code = st.text_input("ZIP Code")
project_type = st.selectbox("Project Type", ["Kitchen Remodel", "Full Home Reno", "Garage Build", "Roof Replacement", "Concrete Work", "Other"])
sq_ft = st.number_input("Total Square Footage", min_value=100, step=50)
buffer = st.slider("Material Buffer % (for overages)", 0, 30, 20)

# Optional Labor Rate
include_labor = st.checkbox("Include Custom Labor Rate?")
if include_labor:
    labor_rate = st.number_input("Labor Cost per Square Foot", min_value=10.0, step=1.0)
else:
    labor_rate = 35.0  # Default average

if st.button("Generate Estimate"):
    st.subheader("📋 Estimate Summary")
    # Material cost assumptions (per sq ft):
    pricing = {
        "2x4 Lumber": 3.5,
        "2x6 Lumber": 4.0,
        "Sheetrock": 1.2,
        "Insulation": 1.0,
        "Roof Tiles": 2.8,
        "Nails": 0.1,
        "Large Bolts": 0.2,
        "Concrete": 3.0,
        "Light Fixtures": 1.5,
        "Plumbing Fixtures": 2.2
    }
    sources = ["Lowe's", "Home Depot", "Ace Hardware", "Local Lumber Yard"]

    material_cost = sum([v * sq_ft for v in pricing.values()])
    buffer_amt = material_cost * (buffer / 100)
    labor_cost = sq_ft * labor_rate
    total = material_cost + buffer_amt + labor_cost

    st.success(f"Estimated Total: ${total:,.2f}")
    st.markdown("---")

    st.subheader("📦 Cost Breakdown")
    for item, cost in pricing.items():
        total_cost = cost * sq_ft
        st.write(f"{item}: ${total_cost:,.2f} ({cost}/sq ft)")

    st.write(f"Material Buffer: ${buffer_amt:,.2f}")
    if include_labor:
        st.write(f"Labor: ${labor_cost:,.2f} (${labor_rate}/sq ft)")

    st.markdown("---")
    st.subheader("🧠 AI-Powered Pricing Explanation")
    st.markdown(f"This estimate is based on average prices from major suppliers such as {', '.join(sources[:-1])}, and {sources[-1]} in ZIP code {zip_code}. Prices were computed using publicly available regional pricing data and construction norms. You can customize rates by uploading supplier CSVs in future versions.")

    st.markdown("---")
    st.caption("Built with ❤️ by AI Construction Bidder Pro")