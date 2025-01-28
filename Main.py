import streamlit as st



data = st.Page(
    "app_pages/0_📋data.py",
    title = "Data",
)
Model = st.Page(
    "app_pages/1_🤖Model.py",
    title="Model",  
)
Prediction = st.Page(
    "app_pages/2_🔮Prediction.py",
    title="Prediction",
)

pg = st.navigation(pages=[data,Model,Prediction])
pg.run()
