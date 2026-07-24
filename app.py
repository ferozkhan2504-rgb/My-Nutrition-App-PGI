import streamlit as st
import pandas as pd

# --- ARJUN BHAGAT DATA: [UnitWt, Energy, Protein, Fat, Carbs, Chol, Fibre, SFA, MUFA, PUFA] ---
food_db = {
    "Chapati with ghee": [25, 4.41, 0.138, 0.076, 0.793, 0.16, 0.021, 0.041, 0.056, 0.024],
    "Chapati dry": [25, 3.90, 0.138, 0.019, 0.793, 0.00, 0.021, 0.003, 0.014, 0.009],
    "Boiled Rice": [150, 0.99, 0.019, 0.001, 0.225, 0.00, 0.040, 0.000, 0.000, 0.000],
    "Pulao / fried rice": [170, 1.58, 0.037, 0.019, 0.313, 0.00, 0.012, 0.002, 0.010, 0.004],
    "Plain Parantha": [30, 3.68, 0.090, 0.137, 0.520, 0.00, 0.014, 0.016, 0.075, 0.031],
    "Stuffed Parantha": [35, 3.06, 0.077, 0.077, 0.514, 0.00, 0.016, 0.009, 0.040, 0.018],
    "Dal with husk": [150, 0.76, 0.030, 0.028, 0.097, 0.00, 0.011, 0.003, 0.015, 0.010],
    "Paneer Gravy": [180, 2.21, 0.115, 0.164, 0.068, 0.08, 0.009, 0.080, 0.037, 0.004],
    "Mix Vegetable": [150, 1.08, 0.021, 0.082, 0.088, 0.00, 0.035, 0.011, 0.015, 0.051],
    "Milk (Full Cream)": [200, 0.67, 0.032, 0.041, 0.044, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Curd": [100, 0.67, 0.031, 0.040, 0.043, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Egg Bhurji": [46, 2.08, 0.156, 0.156, 0.014, 4.98, 0.000, 0.048, 0.059, 0.021],
    "Banana": [100, 1.16, 0.012, 0.003, 0.272, 0.00, 0.004, 0.001, 0.000, 0.000],
}

st.set_page_config(page_title="ICMR Nutrition Tool", layout="wide")

st.title("🏥 Patient Nutrition Assessment (Feroz Style)")
st.caption("Energy, Protein, Fats, Carbs, Chol, Fibre, SFA, MUFA, PUFA Analysis")

# --- 1. PATIENT DEMOGRAPHICS ---
st.header("📋 Patient Identification")
c1, c2, c3, c4 = st.columns(4)
cr_no = c1.text_input("CR Number")
name = c2.text_input("Patient Name")
age = c3.number_input("Age", 1, 100, 45)
mobile = c4.text_input("Mobile No")

c1, c2, c3, c4 = st.columns(4)
height = c1.number_input("Height (cm)", 100.0, 220.0, 170.0)
weight = c2.number_input("Weight (kg)", 10.0, 200.0, 75.0)
gender = c3.selectbox("Gender", ["Male", "Female"])
activity = c4.selectbox("Activity level (IPAQ)", ["Sedentary", "Moderate", "Heavy"])

# BMI Logic
bmi = round(weight / ((height/100)**2), 1)
if bmi < 18.5: status = "Underweight"
elif 18.5 <= bmi < 24.9: status = "Normal"
else: status = "Overweight/Obese"

# --- 2. DIET INTAKE ---
st.header("🥗 Daily Food Recall")
if 'recall' not in st.session_state: st.session_state.recall = []

f1, f2, f3, f4 = st.columns([2, 1, 1, 1])
food = f1.selectbox("Select Food", [""] + list(food_db.keys()))
freq = f2.number_input("Frequency", 0.0, 100.0, 1.0)
unit = f3.selectbox("Timeframe", ["Day", "Week", "Month"])
portion = f4.number_input("Portion (Units)", 0.5, 10.0, 1.0)

if st.button("➕ Add Food"):
    if food: st.session_state.recall.append({"item": food, "freq": freq, "unit": unit, "qty": portion})

# --- 3. FINAL REPORT (Matching Feroz.xlsx) ---
if st.session_state.recall:
    totals = [0.0] * 9 # Energy to PUFA
    for entry in st.session_state.recall:
        mult = 1.0 if entry["unit"] == "Day" else (1/7 if entry["unit"] == "Week" else 1/30)
        grams = entry["freq"] * mult * entry["qty"] * food_db[entry["item"]][0]
        for i in range(9):
            totals[i] += grams * food_db[entry["item"]][i+1]

    # Requirement Logic (Feroz Style)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Male" else -161)
    pal = {"Sedentary": 1.2, "Moderate": 1.5, "Heavy": 1.75}[activity]
    e_req = round(bmr * pal)
    
    targets = [e_req, round(weight*0.9), round((e_req*0.25)/9), round((e_req*0.6)/4), 200, 30, round((e_req*0.08)/9), round((e_req*0.12)/9), round((e_req*0.08)/9)]
    labels = ["Energy (kcal)", "Protein (g)", "Fats (g)", "Carbs (g)", "Cholesterol (mg)", "Fibre (g)", "SFA (g)", "MUFA (g)", "PUFA (g)"]

    st.markdown("### 📊 Requirement (R) vs Intake (In)")
    df = pd.DataFrame({
        "Nutrient": labels,
        "Required (R)": targets,
        "Intake (In)": [round(x, 1) for x in totals]
    })
    df["Difference"] = df["Intake (In)"] - df["Required (R)"]
    st.table(df)
    
    st.info(f"**Health Summary:** Patient is {status} with a BMI of {bmi}.")
    if st.button("Clear Data"):
        st.session_state.recall = []
        st.rerun()
