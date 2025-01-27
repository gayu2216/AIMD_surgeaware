import streamlit as st



data = st.Page(
    "pages/0_📋data.py",
    title = "Data",
)
Model = st.Page(
    "pages/1_🤖Model.py",
    title="Model",  
)
Prediction = st.Page(
    "pages/2_🔮Prediction.py",
    title="Prediction",
)

pg = st.navigation(pages=[data,Model,Prediction])
pg.run()