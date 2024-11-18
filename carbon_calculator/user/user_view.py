import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
import uuid

from carbon_calculator.calculator import calculate_CO2_from_energy_usage, calculate_CO2_from_waste, calculate_CO2_from_business_travel
from carbon_calculator.utils import label, get_csv_download_link, get_image_download_link
from carbon_calculator.user.generate_suggestions import display_suggestions, generate_suggestions
from carbon_calculator.user.validate_inputs import validate_inputs

def user_view():
    st.markdown(
            label(
                icon="leaf.arrow.triangle.circlepath", title="Carbon Footprint Calculator"
            ),
            unsafe_allow_html=True,
        )
    st.markdown(
        """
        <div class='user-sub-header'>
            This tool helps organizations calculate and visualize their carbon footprint across three main categories:
            <ul> 
                <li> Energy Usage </li>
                <li> Waste Management </li>
                <li> Business Travel </li>
            <ul> 
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state variables
    if 'companies_data' not in st.session_state:
        st.session_state.companies_data = []

    # Company Information
    with st.container():
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(
                icon="list.clipboard", title="Company Information", is_subheader=True
            ),
            unsafe_allow_html=True,
        )
        company_name = st.text_input(
            "Company Name", key="company_name", help="Enter your company name"
        )
        report_date = st.date_input("Report Date", datetime.datetime.now())
        st.markdown("</div>", unsafe_allow_html=True)

    # Create three columns for input sections
    col1, col2, col3 = st.columns(3)

    # Energy Usage Section
    with col1:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(icon="bolt.ring.closed", title="Energy Usage", is_subheader=True),
            unsafe_allow_html=True,
        )
        st.session_state.electricity_bill = st.number_input(
            "Monthly Electricity Bill (€)",
            min_value=0.0,
            help="Enter your average monthly electricity bill in euros",
            key="electricity_bill_input"
        )
        st.session_state.natural_gas_bill = st.number_input(
            "Monthly Natural Gas Bill (€)",
            min_value=0.0,
            help="Enter your average monthly natural gas bill in euros",
            key="natural_gas_bill_input"
        )
        st.session_state.fuel_bill = st.number_input(
            "Monthly Fuel Bill (€)",
            min_value=0.0,
            help="Enter your average monthly fuel bill for transportation in euros",
            key="fuel_bill_input"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Waste Section
    with col2:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(icon="arrow.up.trash", title="Waste", is_subheader=True),
            unsafe_allow_html=True,
        )
        st.session_state.waste_per_month = st.number_input(
            "Monthly Waste Generated (kg)",
            min_value=0.0,
            help="Enter the amount of waste generated per month in kilograms",
            key="waste_per_month_input"
        )
        st.session_state.recycling_percent = st.slider(
            "Recycling Percentage",
            min_value=0,
            max_value=100,
            value=30,
            help="Percentage of waste that is recycled or composted",
            key="recycling_percent_input"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Business Travel Section
    with col3:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(icon="airplane.circle", title="Business Travel", is_subheader=True),
            unsafe_allow_html=True,
        )
        st.session_state.distance_km = st.number_input(
            "Distance Traveled (km)",
            min_value=0.0,
            help="Enter the total distance traveled for business purposes in kilometers",
            key="distance_km_input"
        )
        st.session_state.fuel_efficiency = st.number_input(
            "Fuel Efficiency (L/100km)",
            min_value=0.1,
            value=8.0,
            help="Enter the average fuel efficiency in liters per 100 kilometers",
            key="fuel_efficiency_input"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Calculate button
    if st.button("Calculate Carbon Footprint", key="calculate"):
        # Validate all inputs
        is_valid, error_messages = validate_inputs()
        
        if not is_valid:
            for error in error_messages:
                st.error(error)
        else:
            # Proceed with calculations
            CO2_from_energy_usage = calculate_CO2_from_energy_usage(
                st.session_state.electricity_bill,
                st.session_state.natural_gas_bill,
                st.session_state.fuel_bill
            )
            CO2_from_waste = calculate_CO2_from_waste(
                st.session_state.waste_per_month,
                st.session_state.recycling_percent
            )
            CO2_from_business_travel = calculate_CO2_from_business_travel(
                st.session_state.distance_km,
                st.session_state.fuel_efficiency
            )

            # Store data in session state
            report_data = {
                "id": str(uuid.uuid4()),
                "company_name": company_name,
                "date": str(report_date),
                "energy_usage": CO2_from_energy_usage,
                "waste": CO2_from_waste,
                "business_travel": CO2_from_business_travel,
                "total": CO2_from_energy_usage
                + CO2_from_waste
                + CO2_from_business_travel,
            }
            st.session_state.companies_data.append(report_data)

            # Results section
            st.markdown("<div class='results-section'>", unsafe_allow_html=True)
            st.markdown(
                label(
                    icon="chart.bar.xaxis.ascending",
                    title="Carbon Footprint Results",
                    is_subheader=True,
                ),
                unsafe_allow_html=True,
            )

            # Display results in columns
            res_col1, res_col2 = st.columns([2, 1])

            with res_col1:
                # Create pie chart using Plotly
                fig = go.Figure(
                    data=[
                        go.Pie(
                            labels=[
                                "Energy Usage",
                                "Waste Generated",
                                "Business Travel",
                            ],
                            values=[
                                CO2_from_energy_usage,
                                CO2_from_waste,
                                CO2_from_business_travel,
                            ],
                            hole=0.3,
                            marker=dict(colors=["#FF9800", "#4CAF50", "#2196F3"]),
                        )
                    ]
                )

                fig.update_layout(
                    title=f"Carbon Emissions Distribution - {company_name}",
                    annotations=[
                        dict(
                            text="Total kgCO2",
                            x=0.5,
                            y=0.5,
                            font_size=20,
                            showarrow=False,
                        )
                    ],
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})

                # Download buttons for chart
                st.markdown(
                    get_image_download_link(
                        fig,
                        "carbon_footprint_chart.pdf",
                        icon="square.and.arrow.down",
                        text="Download Chart as PDF",
                    ),
                    unsafe_allow_html=True,
                )

            with res_col2:
                # Display detailed results
                st.markdown("### Detailed Breakdown")
                results_df = pd.DataFrame(
                    {
                        "Category": [
                            "Energy Usage",
                            "Waste Generated",
                            "Business Travel",
                        ],
                        "Emissions (kgCO2)": [
                            CO2_from_energy_usage,
                            CO2_from_waste,
                            CO2_from_business_travel,
                        ],
                    }
                )
                results_df["Percentage"] = (
                    results_df["Emissions (kgCO2)"]
                    / results_df["Emissions (kgCO2)"].sum()
                    * 100
                )

                st.dataframe(
                    results_df.style.format(
                        {"Emissions (kgCO2)": "{:.2f}", "Percentage": "{:.1f}%"}
                    ),
                    use_container_width=True,
                )

                total_emissions = results_df["Emissions (kgCO2)"].sum()
                st.metric("Total Carbon Footprint", f"{total_emissions:.2f} kgCO2")

                # Download button for data
                st.markdown(
                    get_csv_download_link(
                        results_df,
                        f"carbon_footprint_data_{company_name}.csv",
                        icon="square.and.arrow.down",
                        text="Download Data as CSV",
                    ),
                    unsafe_allow_html=True,
                )

            # Suggestions section
            suggestions  = generate_suggestions(
                CO2_from_energy_usage,
                CO2_from_waste,
                CO2_from_business_travel,
                st.session_state.electricity_bill,
                st.session_state.natural_gas_bill,
                st.session_state.fuel_bill,
                st.session_state.waste_per_month,
                st.session_state.recycling_percent
            )
            display_suggestions(company_name, suggestions)

            