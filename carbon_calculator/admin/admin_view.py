import streamlit as st
import pandas as pd
import plotly.express as px

from carbon_calculator.utils import label, download_data_button

def admin_view():
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
        download_data_button(df)