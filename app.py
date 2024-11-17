import streamlit as st

from carbon_calculator.user.user_view import user_view
from carbon_calculator.admin.admin_view import admin_view
from carbon_calculator.styles import styles

# Initialize session state for database simulation
if "companies_data" not in st.session_state:
    st.session_state.companies_data = []

# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Calculator", page_icon="🌍", layout="wide"
)

styles()

# User/Admin Selection
user_type = st.sidebar.selectbox("Select User Type", ["Company User", "Admin"])

# User View or Admin View
if user_type == "Company User":
    user_view()
else:
    admin_view()
