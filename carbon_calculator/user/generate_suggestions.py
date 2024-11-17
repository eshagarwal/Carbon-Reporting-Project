import streamlit as st
import pandas as pd

from carbon_calculator.utils import label, get_csv_download_link

# Suggestions Section
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


# bulding ui for suggestions
def display_suggestions(
    company_name,
    suggestions,
):
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

    # Display Priority Actions
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
            st.markdown("Your waste management is effective. Keep up the good work!")

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
    st.markdown(
        get_csv_download_link(
            suggestions_df,
            f"carbon_reduction_suggestions_{company_name}.csv",
            icon="square.and.arrow.down",
            text="Download Suggestions Report",
        ),
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(
        f"""
        By implementing these suggestions, you could potentially reduce your carbon footprint.
        
        Track your progress over time to measure the impact of your reduction efforts.
    """
    )
    st.markdown("</div>", unsafe_allow_html=True)
