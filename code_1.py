import streamlit as st
import pandas as pd
import numpy as np

st.title("Hello World")

with st.sidebar:
    st.header("About the app")
    st.write("This is a simple app to demonstrate the use of Streamlit.")


st.header("This is a header with a divider", divider="rainbow")

st.markdown("*Streamlit* is :red[**really**] ***cool***.")

st.header("st.columns")
col1, col2 = st.columns(2)

with col1:
    x = st.slider("Select a value", 1, 10)

with col2:
    st.write("Selected value: ", x)

st.header("st.charts")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)