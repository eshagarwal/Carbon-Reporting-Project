import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Calculator",
    page_icon="🌍",
    layout="wide"
)

# Title and introduction
st.title("🌍 Corporate Carbon Footprint Calculator")
st.markdown("""
This tool helps organizations calculate and visualize their carbon footprint across three main categories:
- Energy Usage
- Waste Management
- Business Travel

The calculations are based on standardized emission factors and provide estimates in kgCO2.
""")

# Create three columns for input sections
col1, col2, col3 = st.columns(3)

# Energy Usage Section
with col1:
    st.subheader("⚡ Energy Usage")
    electricity_bill = st.number_input(
        "Monthly Electricity Bill (€)",
        min_value=0.0,
        help="Enter your average monthly electricity bill in euros"
    )
    natural_gas_bill = st.number_input(
        "Monthly Natural Gas Bill (€)",
        min_value=0.0,
        help="Enter your average monthly natural gas bill in euros"
    )
    fuel_bill = st.number_input(
        "Monthly Fuel Bill (€)",
        min_value=0.0,
        help="Enter your average monthly fuel bill for transportation in euros"
    )

# Waste Section
with col2:
    st.subheader("🗑️ Waste")
    waste_per_month = st.number_input(
        "Monthly Waste Generated (kg)",
        min_value=0.0,
        help="Enter the amount of waste generated per month in kilograms"
    )
    recycling_percent = st.slider(
        "Recycling Percentage",
        min_value=0,
        max_value=100,
        value=30,
        help="Percentage of waste that is recycled or composted"
    )

# Business Travel Section
with col3:
    st.subheader("✈️ Business Travel")
    distance_km = st.number_input(
        "Distance Traveled (km)",
        min_value=0.0,
        help="Enter the total distance traveled for business purposes in kilometers"
    )
    fuel_efficiency = st.number_input(
        "Fuel Efficiency (L/100km)",
        min_value=0.1,
        value=8.0,
        help="Enter the average fuel efficiency in liters per 100 kilometers"
    )

# Calculation functions
def calculate_CO2_from_energy_usage(electricity_bill, natural_gas_bill, fuel_bill):
    CO2_from_electricity_usage = electricity_bill * 12 * 0.0005
    CO2_from_natural_gas_usage = natural_gas_bill * 12 * 0.0053
    CO2_from_fuel_usage = fuel_bill * 12 * 2.32
    return (CO2_from_electricity_usage + CO2_from_natural_gas_usage + CO2_from_fuel_usage)

def calculate_CO2_from_waste(waste_per_month, recycling_percent):
    return waste_per_month * 12 * 0.57 - recycling_percent

def calculate_CO2_from_business_travel(distance_km, fuel_efficiency):
    return distance_km * 1 / fuel_efficiency * 2.31

# Calculate emissions
if st.button("Calculate Carbon Footprint"):
    CO2_from_energy_usage = calculate_CO2_from_energy_usage(
        electricity_bill, natural_gas_bill, fuel_bill
    )
    CO2_from_waste = calculate_CO2_from_waste(waste_per_month, recycling_percent)
    CO2_from_business_travel = calculate_CO2_from_business_travel(
        distance_km, fuel_efficiency
    )

    # Create results section
    st.markdown("---")
    st.subheader("📊 Carbon Footprint Results")

    # Display results in columns
    res_col1, res_col2 = st.columns([2, 1])

    with res_col1:
        # Create pie chart using Plotly
        fig = go.Figure(data=[go.Pie(
            labels=['Energy Usage', 'Waste Generated', 'Business Travel'],
            values=[CO2_from_energy_usage, CO2_from_waste, CO2_from_business_travel],
            hole=.3
        )])
        
        fig.update_layout(
            title="Carbon Emissions Distribution",
            annotations=[dict(text='Total kgCO2', x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        st.plotly_chart(fig, use_container_width=True)

    with res_col2:
        # Display detailed results
        st.markdown("### Detailed Breakdown")
        results_df = pd.DataFrame({
            'Category': ['Energy Usage', 'Waste Generated', 'Business Travel'],
            'Emissions (kgCO2)': [
                CO2_from_energy_usage,
                CO2_from_waste,
                CO2_from_business_travel
            ]
        })
        results_df['Percentage'] = (
            results_df['Emissions (kgCO2)'] / results_df['Emissions (kgCO2)'].sum() * 100
        )
        
        st.dataframe(
            results_df.style.format({
                'Emissions (kgCO2)': '{:.2f}',
                'Percentage': '{:.1f}%'
            }),
            use_container_width=True
        )

        total_emissions = results_df['Emissions (kgCO2)'].sum()
        st.metric(
            "Total Carbon Footprint",
            f"{total_emissions:.2f} kgCO2"
        )

# Add information about the calculation methodology
with st.expander("ℹ️ Calculation Methodology"):
    st.markdown("""
    ### Emission Factors Used:
    
    1. **Energy Usage**:
        - Electricity: 0.0005 kgCO2/€
        - Natural Gas: 0.0053 kgCO2/€
        - Fuel: 2.32 kgCO2/€

    2. **Waste**:
        - 0.57 kgCO2 per kg of waste
        - Reduced by recycling percentage

    3. **Business Travel**:
        - 2.31 kgCO2 per liter of fuel
        - Adjusted by vehicle efficiency

    These calculations provide estimates based on average emission factors and may vary based on specific circumstances and locations.
    """)