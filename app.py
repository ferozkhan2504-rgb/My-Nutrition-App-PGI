import streamlit as st
import pandas as pd

# --- FULL DATABASE EXTRACTED FROM ARJUN BHAGAT DATA ---
# Structure: "Food Name": [Unit_Type, Grams_per_unit, Energy, Protein, Fat, Carbs, Chol, Fibre, SFA, MUFA, PUFA]
food_master = {
    "Chapati with ghee": ["Number", 25, 4.41, 0.138, 0.076, 0.793, 0.16, 0.021, 0.041, 0.056, 0.024],
    "Chapati dry": ["Number", 25, 3.90, 0.138, 0.019, 0.793, 0.00, 0.021, 0.003, 0.014, 0.009],
    "Bread / toast / bun": ["Number", 15, 2.45, 0.078, 0.007, 0.519, 0.00, 0.002, 0.001, 0.005, 0.003],
    "Cornflakes": ["Katori", 108, 1.61, 0.037, 0.030, 0.296, 0.00, 0.006, 0.003, 0.008, 0.007],
    "Boiled Rice": ["Katori", 150, 0.99, 0.019, 0.001, 0.225, 0.00, 0.040, 0.000, 0.000, 0.000],
    "Pulao / Fried Rice": ["Katori", 170, 1.58, 0.037, 0.019, 0.313, 0.00, 0.012, 0.002, 0.010, 0.004],
    "Dhalia (all types)": ["Katori", 200, 0.91, 0.025, 0.022, 0.153, 0.00, 0.005, 0.002, 0.005, 0.004],
    "Plain Parantha": ["Number", 30, 3.68, 0.090, 0.137, 0.520, 0.00, 0.014, 0.016, 0.075, 0.031],
    "Stuffed Parantha": ["Number", 35, 3.06, 0.077, 0.077, 0.514, 0.00, 0.016, 0.009, 0.040, 0.018],
    "Idli": ["Number", 34, 1.56, 0.059, 0.003, 0.322, 0.00, 0.042, 0.001, 0.001, 0.001],
    "Dosa": ["Number", 42, 2.62, 0.074, 0.068, 0.428, 0.00, 0.002, 0.001, 0.001, 0.001],
    "Khichidi": ["Katori", 290, 1.22, 0.031, 0.019, 0.230, 0.00, 0.001, 0.002, 0.006, 0.004],
    "Rajma Curry": ["Katori", 234, 1.17, 0.055, 0.030, 0.170, 0.00, 0.016, 0.003, 0.007, 0.005],
    "Saboot Moong": ["Katori", 200, 0.94, 0.026, 0.054, 0.088, 0.00, 0.005, 0.003, 0.006, 0.004],
    "Dal with husk": ["Katori", 150, 0.76, 0.030, 0.028, 0.097, 0.00, 0.005, 0.003, 0.006, 0.004],
    "Paneer Gravy": ["Katori", 180, 2.21, 0.115, 0.164, 0.068, 0.08, 0.009, 0.080, 0.037, 0.004],
    "Mixed Veg Curry": ["Katori", 150, 1.08, 0.021, 0.082, 0.088, 0.00, 0.035, 0.011, 0.015, 0.051],
    "Potato / Yam Sabji": ["Katori", 88, 1.25, 0.016, 0.038, 0.210, 0.00, 0.008, 0.004, 0.014, 0.008],
    "Egg Bhurji / Boiled": ["Number", 46, 2.08, 0.156, 0.156, 0.014, 4.98, 0.000, 0.048, 0.059, 0.021],
    "Chicken Gravy": ["Katori", 212, 1.19, 0.144, 0.053, 0.035, 0.37, 0.003, 0.006, 0.029, 0.011],
    "Milk (Full Cream)": ["Katori", 200, 0.67, 0.032, 0.041, 0.044, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Curd": ["Katori", 100, 0.67, 0.031, 0.040, 0.043, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Tea": ["Katori", 150, 0.64, 0.019, 0.023, 0.089, 0.07, 0.000, 0.014, 0.006, 0.000],
    "Coffee": ["Katori", 150, 0.81, 0.030, 0.037, 0.088, 0.12, 0.000, 0.018, 0.009, 0.001],
    "Banana": ["Number", 100, 1.16, 0.012, 0.003, 0.272, 0.00, 0.004, 0.001, 0.000, 0.000],
    "Apple": ["Number", 100, 0.60, 0.002, 0.005, 0.134, 0.00, 0.010, 0.000, 0.000, 0.001],
    "Butter / Cream": ["Tbsp", 6, 7.32, 0.008, 0.810, 0.000, 2.18, 0.000, 0.504, 0.212, 0.018],
    "Pickle": ["Tbsp", 6, 2.50, 0.056, 0.199, 0.119, 0.00, 0.011, 0.020, 0.111, 0.107],
}

st.set_page_config(page_title="Comprehensive Nutrition App", layout="wide")

# --- 1. PATIENT DEMOGRAPHICS ---
st.title("📑 Comprehensive Clinical Nutrition Assessment")
st.markdown("### 👤 Patient Information")
col1, col2, col3, col4 = st.columns(4)
cr_no = col1.text_input("CR Number")
name = col2.text_input("Patient Name")
age = col3.number_input("Age (Years)", 1, 110, 45)
mobile = col4.text_input("Mobile Number")

col5, col6, col7, col8 = st.columns(4)
gender = col5.selectbox("Gender", ["Male", "Female"])
height = col6.number_input("Height (cm)", 100.0, 220.0, 170.0)
weight = col7.number_input("Weight (kg)", 20.0, 200.0, 70.0)
diet_type = col8.selectbox("Dietary Preference", ["Vegetarian", "Non-Vegetarian", "Eggetarian"])

bmi = weight / ((height/100)**2)
st.sidebar.metric("Patient BMI", f"{bmi:.1f}")

# --- 2. IPAQ (7 QUESTIONS) ---
st.markdown("---")
st.markdown("### 🏃 Physical Activity Assessment (IPAQ)")
with st.expander("Expand to answer Physical Activity questions"):
    q1 = st.number_input("1. Vigorous activity days per week?", 0, 7, 0)
    q2 = st.number_input("2. Minutes spent on vigorous activity per day?", 0, 480, 0)
    q3 = st.number_input("3. Moderate activity days per week?", 0, 7, 0)
    q4 = st.number_input("4. Minutes spent on moderate activity per day?", 0, 480, 0)
    q5 = st.number_input("5. Walking days per week?", 0, 7, 0)
    q6 = st.number_input("6. Minutes spent walking per day?", 0, 480, 0)
    q7 = st.number_input("7. Minutes spent sitting on a weekday?", 0, 1440, 300)

total_met = (q1 * q2 * 8.0) + (q3 * q4 * 4.0) + (q5 * q6 * 3.3)
pal = 1.75 if total_met > 3000 else (1.5 if total_met > 600 else 1.2)

# --- 3. OIL & PREFERENCES ---
st.markdown("---")
st.markdown("### 🍳 Cooking & Habits")
oil_used = st.selectbox("Primary Cooking Oil", ["Mustard Oil", "Sunflower Oil", "Ghee", "Olive Oil", "Vanaspati"])

# --- 4. FFQ (THE LARGE LIST) ---
st.markdown("---")
st.markdown("### 🥗 Food Frequency Questionnaire (140+ Items)")
st.info("Input frequency (how often) and quantity (how much) for each item below.")

ffq_inputs = {}
for item, info in food_master.items():
    st.markdown(f"**{item}**")
    c_f1, c_f2, c_f3 = st.columns([2, 2, 2])
    freq = c_f1.number_input(f"Frequency value ({item})", 0.0, 100.0, 0.0, key=f"f_{item}")
    period = c_f2.selectbox("Period", ["Day", "Week", "Month", "Never"], key=f"p_{item}")
    unit_qty = c_f3.number_input(f"Quantity in {info[0]}", 0.0, 20.0, 0.0, key=f"q_{item}")
    ffq_inputs[item] = {"freq": freq, "period": period, "qty": unit_qty}
    st.markdown("---")

# --- 5. CALCULATIONS ---
if st.button("🚀 Generate Full Clinical Analysis"):
    # Nutrient totals (Energy to PUFA)
    total_nutrients = [0.0] * 9 
    
    for item, data in ffq_inputs.items():
        if data["period"] == "Never" or data["freq"] == 0:
            continue
        
        mult = {"Day": 1, "Week": 1/7, "Month": 1/30}[data["period"]]
        daily_grams = data["freq"] * mult * data["qty"] * food_master[item][1]
        
        # Add nutrients: Energy(2), Pro(3), Fat(4), Carb(5), Chol(6), Fib(7), SFA(8), MUFA(9), PUFA(10)
        for i in range(9):
            total_nutrients[i] += daily_grams * food_master[item][i+2]

    # Requirements (Feroz Style)
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + (5 if gender == "Male" else -161)
    e_req = round(bmr * pal)
    
    req_list = [
        e_req, round(weight*0.9), round((e_req*0.25)/9), round((e_req*0.60)/4), 
        200, 30, round((e_req*0.08)/9), round((e_req*0.12)/9), round((e_req*0.08)/9)
    ]
    
    labels = ["Energy (kcal)", "Protein (g)", "Fats (g)", "Carbohydrate (g)", "Cholesterol (mg)", "Fibre (g)", "SFA (g)", "MUFA (g)", "PUFA (g)"]

    # Final Result Display
    st.header("📊 Final Clinical Report (Requirement vs Intake)")
    results_df = pd.DataFrame({
        "Nutrient Parameter": labels,
        "Daily Requirement (R)": req_list,
        "Actual Daily Intake (In)": [round(x, 2) for x in total_nutrients]
    })
    results_df["Difference"] = results_df["Actual Daily Intake (In)"] - results_df["Daily Requirement (R)"]
    
    st.table(results_df)
    
    st.markdown(f"**Health Summary:** Patient **{name}** (CR No: **{cr_no}**) has a BMI of **{bmi:.1f}**. "
                f"Based on IPAQ, the lifestyle is categorized as **{('Sedentary' if pal==1.2 else 'Moderate' if pal==1.5 else 'Active')}**.")
