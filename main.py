# AI Bidder Pro v3 - With User Data Storage, Theme Toggle, and Subscription Trial System
import streamlit as st
from datetime import datetime, timedelta
import json
import os

# --- Dark/Light Mode Toggle ---
theme_mode = st.radio("Choose Theme:", ["Light", "Dark"], horizontal=True)

if theme_mode == "Dark":
    st.markdown("""
        <style>
            body {
                background-color: #0b1d3a;
                color: #ffffff;
            }
            .stButton>button {
                background-color: #1f4f82;
                color: white;
                border-radius: 8px;
                padding: 10px 24px;
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: #f7f7f7;
                color: #000000;
            }
            .stButton>button {
                background-color: #1f4f82;
                color: white;
                border-radius: 8px;
                padding: 10px 24px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Set App Page Config ---
st.set_page_config(page_title="AI Construction Bidder Pro", page_icon="🏗️", layout="centered")

# --- Trial System & Subscription Simulation ---
USERS_FILE = "users.json"
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

with open(USERS_FILE, "r") as f:
    users_data = json.load(f)

st.title("AI Construction Bidder Pro")

if "user" not in st.session_state:
    st.subheader("🔐 Sign In to Access")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Enter App"):
        if name and email:
            if email not in users_data:
                users_data[email] = {
                    "name": name,
                    "start_date": str(datetime.now())
                }
                with open(USERS_FILE, "w") as f:
                    json.dump(users_data, f)

            st.session_state.user = {"name": name, "email": email}
        else:
            st.warning("Please enter both name and email.")
    st.stop()

user_email = st.session_state.user["email"]
user_info = users_data.get(user_email, {})
start_date = datetime.strptime(user_info.get("start_date"), "%Y-%m-%d %H:%M:%S.%f")
trial_days_left = 7 - (datetime.now() - start_date).days

if trial_days_left <= 0:
    st.error("Your 7-day free trial has expired. Please subscribe to continue.")
    st.markdown("[Subscribe Now](https://buy.stripe.com/test_cN27sW5r69HYdGo4gh) 💳")  # Replace with real Stripe/Venmo link
    st.stop()
else:
    st.info(f"Your trial ends in {trial_days_left} day(s). Enjoy! 🎉")

# --- Input Section ---
st.subheader("📝 Project Details")
project_name = st.text_input("Project Name")
zip_code = st.text_input("ZIP Code")
project_type = st.selectbox("Project Type", ["Kitchen Remodel", "Full Home Reno", "Garage Build", "Roof Replacement", "Concrete Work", "Other"])
sq_ft = st.number_input("Total Square Footage", min_value=100, step=50)
buffer = st.slider("Material Buffer % (for overages)", 0, 30, 20)

# --- Project Summary ---
st.subheader("🌐 Project Summary")
project_summary = st.text_area("Project Summary", placeholder="e.g. Kitchen remodel: cabinets, appliances, flooring...")

# --- Materials ---
st.subheader("Materials AI Should Consider")
material_categories = {
    "Lumber": ["2x4", "2x6", "Plywood", "OSB"],
    "Roofing": ["Metal", "Shingles", "Tile", "Asphalt", "Membrane", "Other"],
    "Insulation": ["Fiberglass", "Spray Foam", "Rigid Foam", "Cellulose"],
    "Concrete": ["Foundation", "Driveway", "Sidewalk", "Slab"],
    "Fasteners": ["Nails", "Screws", "Bolts"],
    "Cabinets": ["Stock", "Semi-Custom", "Custom"],
    "Fixtures": ["Plumbing Fixtures", "Lighting Fixtures"],
    "Flooring": ["Hardwood", "Laminate", "Vinyl", "Tile", "Carpet"],
    "Paint": ["Interior", "Exterior"],
    "Trim / Molding": ["Baseboard", "Crown", "Window/Door Trim"],
    "Windows": ["Single Pane", "Double Pane", "Energy Efficient"],
    "Doors": ["Interior", "Exterior", "Custom"],
    "Custom Materials": ["User-Specified"]
}

selected_materials = []
for category, options in material_categories.items():
    with st.expander(category):
        selected = st.multiselect(f"Select {category} materials:", options, key=category)
        selected_materials.extend(selected)

# --- Blueprint Upload ---
uploaded_file = st.file_uploader("Upload your blueprint (PDF, PNG, or JPG)", type=["pdf", "png", "jpg"])
if uploaded_file:
    st.success(f"Uploaded: {uploaded_file.name}")

# --- Optional Labor Rate ---
include_labor = st.checkbox("Include Custom Labor Rate?")
if include_labor:
    labor_rate = st.number_input("Labor Cost per Square Foot", min_value=10.0, step=1.0)
else:
    labor_rate = 35.0  # Default rate

# --- Run Estimation ---
if st.button("Generate Estimate"):
    st.subheader("📋 Estimate Summary")
    pricing = {
        "2x4 Lumber": 3.5,
        "2x6 Lumber": 4.0,
        "Sheetrock": 1.2,
        "Insulation": 1.0,
        "Roof Tiles": 2.8,
        "Nails": 0.1,
        "Screws": 0.12,
        "Bolts": 0.2,
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
    st.subheader("📦 Cost Breakdown")
    for item, cost in pricing.items():
        st.write(f"{item}: ${cost * sq_ft:,.2f} ({cost}/sq ft)")
    st.write(f"Material Buffer: ${buffer_amt:,.2f}")
    st.write(f"Labor: ${labor_cost:,.2f}")

    st.markdown("---")
    st.subheader("🧐 AI-Powered Pricing Explanation")
    st.markdown(f"Estimate based on prices from {', '.join(sources)} in ZIP code {zip_code}.")

st.markdown("---")
st.caption("Built with ❤️ by AI Construction Bidder Pro")


