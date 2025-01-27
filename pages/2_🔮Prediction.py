import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go


st.set_page_config(layout="wide")

if "risk_score" not in st.session_state:
    st.session_state["risk_score"] = "" 

if "text" not in st.session_state:
     st.session_state["text"]=""

if "complication" not in st.session_state:
     st.session_state["comlication"]=""
     

col1, col2, col3 = st.columns([1,2,3])


with col1:
    st.image("/Users/gayathriutla/Desktop/Projects/AIMD-surgeaware/logo_final.jpeg", width=150)  # Adjust width as needed




model1 = joblib.load('first_model.pkl')
model2 = joblib.load('second_model.pkl')

with col2:

            BIRTH_DATE = st.slider("Age(in years)", min_value=0, max_value=100,key=1)
            weight = st.number_input("Weight(in kgs)", placeholder="Type here...",key=2)
            ASA_RATING_C = st.selectbox(
                        "ASA_RATING:",
                        options=[1,2,3,4,5,6],key=3
                        )
            GENDER= st.radio(
            "Gender:",
            options=["Male", "Female"],key=4
            )
            ICU_ADMIN_FLAG= st.radio(
            "Was admitted in ICU:",
            options=["Yes", "No"],key=5
            )
            LOS = st.text_input("Length of stay", placeholder="Type here...",key=6)
            #ICU_ADMIN_FLAG,LOS,BIRTH_DATE,WEIGHT,SEX,ASA_RATING_C,DISCH_DISP,diagnosis_code

            gender_map = {"Male": 1, "Female": 0}
            icu_map = {"Yes":1,"No":0}
            MALE = gender_map[GENDER]
            YES = icu_map[ICU_ADMIN_FLAG]
            WEIGHT = (weight*35.27396195)


            input_data1 ={'LOS':LOS,
            'BIRTH_DATE': BIRTH_DATE,
            'WEIGHT' : WEIGHT,
            'ASA_RATING_C':ASA_RATING_C,
            'Male':MALE,
            'Yes':YES
            }
            #ICU_ADMIN_FLAG,LOS,BIRTH_DATE,WEIGHT,SEX,ASA_RATING_C,Element_Name
            input_data2 ={'LOS':LOS,
                        'BIRTH_DATE': BIRTH_DATE,
                        'WEIGHT' : WEIGHT,
                        'ASA_RATING_C':ASA_RATING_C,
                        'Male':MALE,
                        'Yes':YES
                        }

            input_row = pd.DataFrame(input_data1,index=[0])
            input_row1 = pd.DataFrame(input_data2,index=[0])

            if st.button("Predict"):
                prediction = model1.predict(input_row)
                risk_value = {'Home Routine': 20,      #### need to us prediction to display the risk value
                                'Hospice Facility': 90,
                                'Skilled Nursing Facility': 75,
                                'Home Healthcare IP Admit Related': 35,
                                'Rehab Facility (this hospital)': 60,
                                'Expired': 100,
                                'Acute Care Facility (not this hospital)': 80,
                                'Long Term Care Facility': 70,
                                'Rehab Facility (not this hospital)': 65,
                                'Psychiatric Facility (this hospital)': 55,
                                None: 0, 
                                "Cancer Ctr/Children's Hospital": 70,
                                'Acute Care Facility (this hospital)': 75,
                                'Hospice Home': 85,
                                'Federal Hospital': 70,
                                'Coroner': 100,
                                'Recuperative Care': 70,
                                'Sub-Acute Care Facility': 65,
                                'Board and Care': 55,
                                'Intermediate/Residential Care Facility': 60,
                                'Home Healthcare Outside 3 Days': 40,
                                'Intermediate/Residential Care w Planned Readmit': 75,
                                'Psychiatric Facility (not this hospital)': 60,
                                'Critical Access Hospital': 75,
                                'Home Health w Planned Readmit': 55,
                                'Designated Disaster Alternative Care Site': 80,
                                'Home Healthcare Outpatient Related': 30,
                                'Federal Hospital w Planned Readmit': 80,
                                'Designated Disaster Alternate Care Site': 80,
                                'Temporary Living': 65,
                                'Skilled Nursing w Planned Readmit': 85,
                                'Independent Living': 25,
                                'Room and Board': 30}
                risk_score= risk_value[prediction[0]]
                st.session_state.risk_score= risk_score
                prediction1 = model2.predict(input_row1)
                poc = prediction1[0]
                st.session_state["comlication"]= poc
                

                import google.generativeai as genai
                genai.configure(api_key="AIzaSyANoozGpKymmSgtUlS8SzyL8WJVbTOC1Zo")
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(f"You are an AI assistant integrated with a validated surgical risk prediction model. Based on the risk scores {risk_score} for {poc} for a patient with the following characteristics: age {BIRTH_DATE},asa_rating {ASA_RATING_C},WEIGHT IN onces{WEIGHT},gender {GENDER}, generated by the model, provide a tailored response for healthcare professionals to consider. The risk score for post-surgical complications is [X]. Offer suggestions for potential post-operative care strategies, focusing on general best practices and areas of attention for the medical team. Remember, this information is meant to support, not replace, professional medical judgment.Format this as a bulleted list, removing all introductory and concluding paragraphs, and focusing solely on the actionable post-operative points. Prioritize the list with items related to immediate complications and patient risk factors (obesity, ASA 3) appearing higher. Do not include any sentences that are not actionable and remove the bullet point at the begining of every category. Finally make sure there are no extra spaces between the points")
                text = response.text
                st.session_state.text = text
            

with col3:
        if st.session_state.risk_score and st.session_state.text:
            remaining_score = 100-st.session_state.risk_score
            labels = ["Risk", "Remaining"]
            values = [st.session_state.risk_score, remaining_score]

            if st.session_state.risk_score < 40:
                color = "green" 
            elif st.session_state.risk_score < 70:
                color = "orange"  
            else:
                color = "red"  


            fig = go.Figure(
                data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.5, 
                marker=dict(colors=[color, "lightgrey"]), 
                textinfo="none"   
                )])

            fig.update_layout(
                title="Risk Score",
                annotations=[
                    dict(
                        text=f"{st.session_state.risk_score}", 
                        font_size=40,
                        showarrow=False
                    )
                ],
                showlegend=False
            )


            st.plotly_chart(fig)

            with st.expander("Postoperative complication:"):
                #with st.container(height=50):

                    if st.session_state.comlication == "AN AQI POST-OP COMPLICATIONS":
                        st.write("AN Analgesia Quality Index POST-OP COMPLICATIONS")
                    else:
                        st.write(f"{st.session_state.comlication}")

        

            with st.expander("Suggestions:"):
                with st.container(height=300):
                    st.write(st.session_state.text)
            
        else:
            st.write("")

