import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import json
import base64
from io import BytesIO
import uuid

# Initialize session state for database simulation
if "companies_data" not in st.session_state:
    st.session_state.companies_data = []

# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Calculator", page_icon="🌍", layout="wide"
)

# Custom CSS for styling
st.markdown(
    """
<style>
    .stApp {
        background-color: #f5f7f9;
    }
    .input-section {
        border-top: 2px solid #dddddd;
    }
    .results-section {
        border-top: 2px solid #dddddd;
    }
    .admin-card {
        border-top: 2px solid #dddddd;
    }
    .user-sub-header {
        background-color: #e3f2fd; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 20px;
    }
    .custom-icon-header {
        height: 40px; 
        width: auto;
    }
    .custom-icon-sub-header {
        height: 25px; 
        width: auto;
    }
</style>
""",
    unsafe_allow_html=True,
)

# User/Admin Selection
user_type = st.sidebar.selectbox("Select User Type", ["Company User", "Admin"])


def label(icon: str, title: str, is_subheader: bool = False) -> str:
    icon_class = "custom-icon-sub-header" if is_subheader else "custom-icon-header"
    return f"""
    {'<h3>' if is_subheader else '<h1>'}
        <img class='{icon_class}' src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/{icon}.png'/>
        {title}
    {'</h3>' if is_subheader else '</h1>'}
"""


# User View
if user_type == "Company User":
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
        electricity_bill = st.number_input(
            "Monthly Electricity Bill (€)",
            min_value=0.0,
            help="Enter your average monthly electricity bill in euros",
        )
        natural_gas_bill = st.number_input(
            "Monthly Natural Gas Bill (€)",
            min_value=0.0,
            help="Enter your average monthly natural gas bill in euros",
        )
        fuel_bill = st.number_input(
            "Monthly Fuel Bill (€)",
            min_value=0.0,
            help="Enter your average monthly fuel bill for transportation in euros",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Waste Section
    with col2:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(icon="arrow.up.trash", title="Waste", is_subheader=True),
            unsafe_allow_html=True,
        )
        waste_per_month = st.number_input(
            "Monthly Waste Generated (kg)",
            min_value=0.0,
            help="Enter the amount of waste generated per month in kilograms",
        )
        recycling_percent = st.slider(
            "Recycling Percentage",
            min_value=0,
            max_value=100,
            value=30,
            help="Percentage of waste that is recycled or composted",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Business Travel Section
    with col3:
        st.markdown("<div class='input-section'>", unsafe_allow_html=True)
        st.markdown(
            label(icon="airplane.circle", title="Business Travel", is_subheader=True),
            unsafe_allow_html=True,
        )
        distance_km = st.number_input(
            "Distance Traveled (km)",
            min_value=0.0,
            help="Enter the total distance traveled for business purposes in kilometers",
        )
        fuel_efficiency = st.number_input(
            "Fuel Efficiency (L/100km)",
            min_value=0.1,
            value=8.0,
            help="Enter the average fuel efficiency in liters per 100 kilometers",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Calculation functions
    def calculate_CO2_from_energy_usage(electricity_bill, natural_gas_bill, fuel_bill):
        CO2_from_electricity_usage = electricity_bill * 12 * 0.0005
        CO2_from_natural_gas_usage = natural_gas_bill * 12 * 0.0053
        CO2_from_fuel_usage = fuel_bill * 12 * 2.32
        return (
            CO2_from_electricity_usage
            + CO2_from_natural_gas_usage
            + CO2_from_fuel_usage
        )

    def calculate_CO2_from_waste(waste_per_month, recycling_percent):
        return waste_per_month * 12 * 0.57 - recycling_percent

    def calculate_CO2_from_business_travel(distance_km, fuel_efficiency):
        return distance_km * 1 / fuel_efficiency * 2.31

    def generate_suggestions(
        energy_usage,
        waste,
        business_travel,
        electricity_bill,
        natural_gas_bill,
        fuel_bill,
        waste_per_month,
        recycling_percent,
    ):
        """Generate tailored suggestions based on the company's carbon footprint data."""
        suggestions = {"energy": [], "waste": [], "travel": [], "priority_actions": []}

        # Energy Usage Suggestions
        if electricity_bill > 1000:
            suggestions["energy"].extend(
                [
                    "Install LED lighting throughout your facilities",
                    "Implement motion sensors for lighting in less frequently used areas",
                    "Consider solar panel installation for renewable energy generation",
                    "Conduct an energy audit to identify major consumption areas",
                ]
            )
        if natural_gas_bill > 500:
            suggestions["energy"].extend(
                [
                    "Improve building insulation to reduce heating/cooling needs",
                    "Install a smart thermostat system",
                    "Regular maintenance of HVAC systems",
                    "Consider heat pump technology for heating and cooling",
                ]
            )
        if fuel_bill > 800:
            suggestions["energy"].extend(
                [
                    "Transition to electric or hybrid vehicles for company fleet",
                    "Implement a vehicle maintenance schedule",
                    "Install energy-efficient heating/cooling systems",
                ]
            )

        # Waste Suggestions
        if recycling_percent < 50:
            suggestions["waste"].extend(
                [
                    f"Increase recycling rate (currently {recycling_percent}%). Target: 75%",
                    "Implement a comprehensive recycling program",
                    "Train employees on proper waste segregation",
                    "Partner with recycling services for different waste streams",
                ]
            )
        if waste_per_month > 1000:
            suggestions["waste"].extend(
                [
                    "Implement a paperless office policy",
                    "Start a composting program for organic waste",
                    "Set up double-sided printing as default",
                    "Create a waste reduction awareness campaign",
                ]
            )

        # Business Travel Suggestions
        if business_travel > 1000:
            suggestions["travel"].extend(
                [
                    "Promote virtual meetings over physical travel",
                    "Implement a travel optimization system",
                    "Consider carbon offsetting for necessary travel",
                    "Develop a green travel policy",
                ]
            )

        # Determine Priority Actions
        total_emissions = energy_usage + waste + business_travel
        emissions_breakdown = {
            "Energy Usage": energy_usage,
            "Waste": waste,
            "Business Travel": business_travel,
        }

        # Sort emissions by highest to lowest
        sorted_emissions = sorted(
            emissions_breakdown.items(), key=lambda x: x[1], reverse=True
        )

        # Add priority actions based on highest emission areas
        suggestions["priority_actions"] = [
            f"Focus on {sorted_emissions[0][0]}: Highest impact area ({sorted_emissions[0][1]:.2f} kgCO2)",
            f"Secondary focus on {sorted_emissions[1][0]}: ({sorted_emissions[1][1]:.2f} kgCO2)",
            f"Monitor {sorted_emissions[2][0]}: ({sorted_emissions[2][1]:.2f} kgCO2)",
        ]

        return suggestions

    # Download functions
    def get_image_download_link(fig, filename, icon, text):
        buf = BytesIO()
        fig.write_image(buf, format="pdf")
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode()
        href = f"""
        <img style="height: 20px; width: auto" src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/{icon}.png'/>
        <a href="data:application/pdf;base64,{b64}" download="{filename}.pdf">
            {text}
        </a>
        """
        return href

    def get_csv_download_link(df, filename, icon, text):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f"""
        <img style="height: 20px; width: auto" src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/{icon}.png'/>
        <a href="data:application/pdf;base64,{b64}" download="{filename}">
            {text}
        </a>
        """
        return href

    # Calculate button
    if st.button("Calculate Carbon Footprint", key="calculate"):
        if not company_name:
            st.error("Please enter a company name before calculating.")
        else:
            CO2_from_energy_usage = calculate_CO2_from_energy_usage(
                electricity_bill, natural_gas_bill, fuel_bill
            )
            CO2_from_waste = calculate_CO2_from_waste(
                waste_per_month, recycling_percent
            )
            CO2_from_business_travel = calculate_CO2_from_business_travel(
                distance_km, fuel_efficiency
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

                st.plotly_chart(fig, use_container_width=True)

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

            # Suggestions Section
            st.markdown("<div class='results-section'>", unsafe_allow_html=True)
            st.markdown(
                label(
                    icon="leaf",
                    title="Emission Reduction Suggestions",
                    is_subheader=True,
                ),
                unsafe_allow_html=True,
            )

            suggestions = generate_suggestions(
                CO2_from_energy_usage,
                CO2_from_waste,
                CO2_from_business_travel,
                electricity_bill,
                natural_gas_bill,
                fuel_bill,
                waste_per_month,
                recycling_percent,
            )

            # Display Priority Actions
            # st.markdown(label(icon='custom.target.badge.exclamationmark', title='Priority Actions', is_subheader=True), unsafe_allow_html=True)
            for action in suggestions["priority_actions"]:
                st.markdown(f"- {action}")

            # Create tabs for detailed suggestions
            tab1, tab2, tab3 = st.tabs(["Energy", "Waste", "Travel"])

            with tab1:
                if suggestions["energy"]:
                    for suggestion in suggestions["energy"]:
                        st.markdown(f"- {suggestion}")
                else:
                    st.markdown(
                        "Your energy usage is relatively efficient. Continue monitoring!"
                    )

            with tab2:
                if suggestions["waste"]:
                    for suggestion in suggestions["waste"]:
                        st.markdown(f"- {suggestion}")
                else:
                    st.markdown(
                        "Your waste management is effective. Keep up the good work!"
                    )

            with tab3:
                if suggestions["travel"]:
                    for suggestion in suggestions["travel"]:
                        st.markdown(f"- {suggestion}")
                else:
                    st.markdown("Your business travel emissions are well managed!")

            # Add a download button for the suggestions
            suggestions_df = pd.DataFrame(
                {
                    "Category": ["Priority Actions", "Energy", "Waste", "Travel"],
                    "Suggestions": [
                        "\n".join(suggestions["priority_actions"]),
                        "\n".join(suggestions["energy"]),
                        "\n".join(suggestions["waste"]),
                        "\n".join(suggestions["travel"]),
                    ],
                }
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                get_csv_download_link(
                    suggestions_df,
                    f"carbon_reduction_suggestions_{company_name}.csv",
                    icon="square.and.arrow.down",
                    text="Download Suggestions Report",
                ),
                unsafe_allow_html=True,
            )

            # Add an estimation of potential reduction
            potential_reduction = (
                total_emissions * 0.3
            )  # Assuming 30% reduction potential
            st.info(
                f"""
                By implementing these suggestions, you could potentially reduce your carbon footprint by up to 
                {potential_reduction:.2f} kgCO2 (30% reduction).
                
                Track your progress over time to measure the impact of your reduction efforts.
            """
            )
            st.markdown("</div>", unsafe_allow_html=True)


else:  # Admin View
    def download_data_button():
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f"""
        <img style="height: 20px; width: auto" src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/square.and.arrow.down.png'/>
        <a href="data:file/csv;base64,{b64}" download="complete_carbon_footprint_data.csv">
        Click here to download the complete dataset
        </a>
        """
        st.markdown(href, unsafe_allow_html=True)
    st.markdown(label(icon="person.badge.key", title="Admin Dashboard"), unsafe_allow_html=True)

    if not st.session_state.companies_data:
        st.warning("No company data available yet.")
    else:
        # Convert session state data to DataFrame
        df = pd.DataFrame(st.session_state.companies_data)

        # Overview metrics
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Companies", len(df["company_name"].unique()))
        with col2:
            st.metric("Total Reports", len(df))
        with col3:
            st.metric("Total Emissions", f"{df['total'].sum():.2f} kgCO2")
        st.markdown("</div>", unsafe_allow_html=True)

        # Historical Data
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.markdown(label(icon="chart.line.uptrend.xyaxis", title="Historical Data", is_subheader=True), unsafe_allow_html=True)
        st.dataframe(
            df.style.format(
                {
                    "energy_usage": "{:.2f}",
                    "waste": "{:.2f}",
                    "business_travel": "{:.2f}",
                    "total": "{:.2f}",
                }
            ),
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Company Comparison
        st.markdown("<div class='admin-card'>", unsafe_allow_html=True)
        st.markdown(label(icon="magnifyingglass.circle", title="Company Comparison", is_subheader=True), unsafe_allow_html=True)
        fig = px.bar(
            df,
            x="company_name",
            y=["energy_usage", "waste", "business_travel"],
            title="Emissions by Company",
            labels={"value": "Emissions (kgCO2)", "company_name": "Company"},
            barmode="stack",
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download complete dataset
        download_data_button()
