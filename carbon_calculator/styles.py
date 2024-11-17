import streamlit as st


def styles():
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
