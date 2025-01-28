
import streamlit as st


st.set_page_config(layout="wide")


col1, col2, col3 = st.columns([1,4,1])



with col1:
    st.image("logo_final.jpeg", width=150)  # Adjust width as needed

with col2:
    st.write("")
    st.write("")

    st.title("MOVER Dataset Overview")

   

    st.subheader("📊 Key Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("👤 **Patient Data:** Information from 58,799 unique patients")
        st.markdown("🏫 **Location:** University of California, Irvine Medical Center")

    with col2:
        st.markdown("🏥 **Surgeries:** Data from 83,468 surgeries")
        st.markdown("📅 **Time Period:** 2015–2022")

    st.subheader("🔍 Dataset Features")

    features = {
        "🎂 BIRTH_DATE": "Patient age in years",
        "⚖️ WEIGHT": "Patient weight (ounces for EPIC dataset)",
        "⚧️ SEX": "Genotypical sex of the patient",
        "📝 ASA_RATING": "Name for each ASA class",
        "🏥 ICU_ADMIN": "Indicates ICU admission during visit",
        "🔢 DIAGNOSIS_CODE": "ICD-9-CM codes for patient diagnoses"
    }

    for feature, description in features.items():
        st.markdown(f"**{feature}:** {description}")

    st.markdown("---")

    st.title("Approach Overview")

    st.header("Machine Learning Models:")

    st.markdown("""
    1. **Risk Factor Calculation Model**:
        - This model calculates the patient's risk factor based on available data such as age, medical history, and pre-surgery risk factors.
        -  Algorithm: Random Forest Classifier
    """)

    st.markdown("""
    2. **Post-Operative Complication Prediction Model**:
        -  This model predicts possible post-operative complications based on the calculated risk factor.
         \-  Algorithm: Random Forest Classifier
    """)

    st.header("GEMINI API:")

    st.markdown("""
        -  The GEMINI API is integrated to provide post-operative care recommendations.
        -  It takes the risk factors and complications predicted by the models and suggests appropriate care strategies.
    """)

