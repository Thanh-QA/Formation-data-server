import streamlit as st
import requests
import pandas as pd

process = st.text_input("Process")

if process:
    r = requests.get(
        "https://ocv-api.onrender.com/lookup",
        params={"process": process}
    )
    df = pd.DataFrame(r.json())
    st.dataframe(df)
