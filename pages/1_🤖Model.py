import json
import requests
import streamlit as st
import pandas as pd
import joblib
from streamlit_lottie import st_lottie_spinner 



st.set_page_config(layout="wide")

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)

logo = load_lottiefile("ann.json")

col1, col2, col3 = st.columns([1,4,1])


with col1:
    st.image("logo_final.jpeg", width=150)  # Adjust width as needed


patient_data = pd.read_csv("first_data.csv.zip")
patient_postop_data = pd.read_csv("second_data.csv.zip")
patient_postop_data = patient_postop_data.reset_index(drop=True)

icd9_codes = {
    "Gastroesophageal reflux disease": "530.81",
    "Hypothyroidism": "244.9",
    "Chronic obstructive pulmonary disease": "496",
    "Osteoporosis": "733.00",
    "Inguinal hernia": "550.90",
    "Cataract": "366.9",
    "Appendicitis": "540.9",
    "Gallstones": "574.20",
    "Diverticulosis of colon": "562.10",
    "Benign prostatic hyperplasia": "600.00",
    "Knee osteoarthritis": "715.16",
    "Hip osteoarthritis": "715.15",
    "Spinal stenosis": "724.02",
    "Rotator cuff syndrome": "726.10",
    "Carpal tunnel syndrome": "354.0",
    "Attention deficit disorder with hyperactivity": "314.01",
    "Asthma, unspecified": "493.90",
    "Chest pain, unspecified": "786.50",
    "Hypertension, essential": "401.9",
    "Uterine prolapse": "618.04",
    "Urinary tract infection": "599.0",
    "Breast lump or mass": "611.72",
    "Depressive disorder": "311",
    "Melanoma of skin": "172.9",
    "Atrial fibrillation": "427.31",
    "Coronary atherosclerosis": "414.00",
    "Plantar fasciitis": "728.71",
    "Bunion": "727.1",
    "Hammer toe": "735.4",
    "Ingrown toenail": "703.0",
    "Breast cancer": "174.9",
    "Prostate cancer": "185",
    "Colon cancer": "153.9",
    "Lung cancer": "162.9",
    "Skin cancer": "173.9",
    "Ovarian cancer": "183.0",
    "Uterine cancer": "182.0",
    "Bladder cancer": "188.9",
    "Kidney cancer": "189.0",
    "Thyroid cancer": "193",
    "Brain tumor": "191.9",
    "Abdominal aortic aneurysm": "441.4",
    "Carotid artery stenosis": "433.10",
    "Peripheral vascular disease": "443.9",
    "Varicose veins": "454.9",
    "Deep vein thrombosis": "453.40",
    "Pulmonary embolism": "415.19",
    "Cerebral aneurysm": "437.3",
    "Intracranial hemorrhage": "431",
    "Subdural hematoma": "432.1",
    "Acute myocardial infarction": "410.90",
    "Congestive heart failure": "428.0",
    "Aortic valve stenosis": "424.1",
    "Mitral valve prolapse": "424.0",
    "Pericarditis": "423.9",
    "Cardiac tamponade": "423.3",
    "Pneumothorax": "512.8",
    "Pleural effusion": "511.9",
    "Empyema": "510.9",
    "Lung abscess": "513.0",
    "Pneumonia": "486",
    "Tuberculosis of lung": "011.90",
    "Pulmonary fibrosis": "515",
    "Acute respiratory failure": "518.81",
    "Gastric ulcer": "531.90",
    "Duodenal ulcer": "532.90",
    "Gastritis": "535.50",
    "Small intestinal obstruction": "560.9",
    "Crohn's disease": "555.9",
    "Ulcerative colitis": "556.9",
    "Acute pancreatitis": "577.0",
    "Chronic pancreatitis": "577.1",
    "Cirrhosis of liver": "571.5",
    "Cholelithiasis": "574.20",
    "Cholecystitis": "575.10",
    "Acute appendicitis": "540.9",
    "Peritonitis": "567.9",
    "Inguinal hernia": "550.90",
    "Femoral hernia": "553.00",
    "Umbilical hernia": "553.1",
    "Ventral hernia": "553.21",
    "Intestinal adhesions": "560.81",
    "Hemorrhoids": "455.6",
    "Anal fissure": "565.0",
    "Perianal abscess": "566",
    "Pilonidal cyst": "685.1",
    "Hydronephrosis": "591",
    "Kidney stones": "592.0",
    "Bladder stones": "594.1",
    "Urethral stricture": "598.9",
    "Testicular torsion": "608.20",
    "Hydrocele": "603.9",
    "Varicocele": "456.4",
    "Prostatitis": "601.9",
    "Endometriosis": "617.9",
    "Uterine fibroids": "218.9",
    "Ovarian cyst": "620.2",
    "Pelvic inflammatory disease": "614.9",
    "Cervical dysplasia": "622.10",
    "Vaginal prolapse": "618.00",
    "Bartholin's cyst": "616.2",
    "Ectopic pregnancy": "633.90",
    "Placenta previa": "641.10",
    "Cervical incompetence": "654.50",
    "Intrauterine growth restriction": "656.50",
    "Preeclampsia": "642.40",
    "Gestational diabetes": "648.80",
    "Multiple gestation": "651.00",
    "Postpartum hemorrhage": "666.10",
    "Mastitis": "675.90",
    "Breast abscess": "611.0",
    "Fracture of clavicle": "810.00",
    "Fracture of humerus": "812.00",
    "Fracture of radius and ulna": "813.80",
    "Fracture of hand bones": "814.00",
    "Fracture of vertebral column": "805.8",
    "Fracture of pelvis": "808.8",
    "Fracture of femur": "821.00",
    "Fracture of patella": "822.0",
    "Fracture of tibia and fibula": "823.80",
    "Fracture of ankle": "824.8",
    "Fracture of foot bones": "825.25",
    "Dislocation of shoulder": "831.00",
    "Dislocation of elbow": "832.00",
    "Dislocation of hip": "835.00",
    "Dislocation of knee": "836.3",
    "Torn meniscus of knee": "836.0",
    "Sprain of ankle and foot": "845.00",
    "Concussion": "850.0",
    "Intracranial injury": "854.00",
    "Open wound of head": "873.0",
    "Open wound of neck": "874.8",
    "Open wound of chest": "875.0",
    "Open wound of back": "876.0",
    "Open wound of buttock": "877.0",
    "Burn of face, head, and neck": "941.00",
    "Burn of trunk": "942.00",
    "Burn of upper limb": "943.00",
    "Burn of lower limb": "945.00",
    "Burn of multiple specified sites": "946.0",
    "Frostbite": "991.0",
    "Drowning and nonfatal submersion": "994.1",
    "Toxic effect of carbon monoxide": "986",
    "Toxic effect of alcohol": "980.0"
}

k = icd9_codes.keys()

with col2:
    sname = st.selectbox("Diagnosis Name", options=k,placeholder="...")
    diagnosis_code = icd9_codes[sname]
    diagnosis_code = float(diagnosis_code)


    if st.button("Train Model"):
        with st_lottie_spinner(logo, key="spinner"):
            patient_data['diagnosis_code'] = pd.to_numeric(patient_data['diagnosis_code'], errors='coerce')
            data = patient_data[patient_data["diagnosis_code"]==diagnosis_code]
            data = data.drop("diagnosis_code",axis=1)
            X = data.drop("DISCH_DISP",axis=1)
            y = data["DISCH_DISP"]
            from sklearn.ensemble import RandomForestClassifier
            rp = RandomForestClassifier(n_estimators=200)
            rp.fit(X,y)
            patient_postop_data['diagnosis_code'] = pd.to_numeric(patient_postop_data['diagnosis_code'], errors='coerce')
            data_p = patient_postop_data[patient_postop_data["diagnosis_code"]==diagnosis_code]
            data_p = data_p.drop("diagnosis_code",axis=1)
            X1 = data_p.drop("Element_Name",axis=1)
            y1 = data_p["Element_Name"]
            pop = RandomForestClassifier(n_estimators=200) 
            pop.fit(X1,y1)
            if rp and pop:
                joblib.dump(rp,'first_model.pkl')
                joblib.dump(pop,'second_model.pkl')
                st.switch_page("pages/2_🔮Prediction.py")
                st.session_state.shared_variable = diagnosis_code
                with open("/Users/gayathriutla/Desktop/Projects/AIMD-surgeaware/multipage/ann.json", "r") as f:
                    json.load(f)
                
            else:
                st.write("Please Enter diagonis code")
