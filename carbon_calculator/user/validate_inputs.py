import streamlit as st

def validate_inputs():
    """Validate all inputs and return a tuple of (is_valid, error_messages)"""
    is_valid = True
    error_messages = []
    
    # Company Information validation
    if not st.session_state.company_name:
        is_valid = False
        error_messages.append("Please enter a company name.")

    # Energy Usage validation
    if st.session_state.electricity_bill == 0 and st.session_state.natural_gas_bill == 0 and st.session_state.fuel_bill == 0:
        is_valid = False
        error_messages.append("Please enter at least one energy usage value.")
    
    # Waste validation
    if st.session_state.waste_per_month == 0:
        is_valid = False
        error_messages.append("Please enter the amount of waste generated.")
    
    # Business Travel validation
    if st.session_state.distance_km == 0:
        is_valid = False
        error_messages.append("Please enter the distance traveled.")
    if st.session_state.fuel_efficiency <= 0:
        is_valid = False
        error_messages.append("Please enter a valid fuel efficiency value greater than 0.")
        
    return is_valid, error_messages