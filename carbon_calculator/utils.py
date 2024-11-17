import streamlit as st

from io import BytesIO
import base64

def label(icon: str, title: str, is_subheader: bool = False) -> str:
    icon_class = "custom-icon-sub-header" if is_subheader else "custom-icon-header"
    return f"""
    {'<h3>' if is_subheader else '<h1>'}
        <img class='{icon_class}' src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/{icon}.png'/>
        {title}
    {'</h3>' if is_subheader else '</h1>'}
"""

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

def download_data_button(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f"""
    <img style="height: 20px; width: auto" src='https://raw.githubusercontent.com/eshagarwal/Carbon-Reporting-Project/main/Icons/square.and.arrow.down.png'/>
    <a href="data:file/csv;base64,{b64}" download="complete_carbon_footprint_data.csv">
    Click here to download the complete dataset
    </a>
    """
    return st.markdown(href, unsafe_allow_html=True)