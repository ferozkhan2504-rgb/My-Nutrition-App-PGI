import streamlit as st
import pandas as pd

# --- FULL FOOD DATABASE (Extracted from your data) ---
# Format: "Food Name": [Unit Weight(g), Energy/g, Protein/g, Fat/g, Carbs/g]
food_data = {
    "Chapati with ghee": [25, 4.41, 0.138, 0.076, 0.793],
    "Chapati dry": [25, 3.90, 0.138, 0.019, 0.793],
    "Bread/Buns": [15, 2.45, 0.078, 0.007, 0.519],
    "Cornflakes": [108, 1.61, 0.037, 0.030, 0.296],
    "Boiled Rice": [150, 0.99, 0.019, 0.001, 0.225],
    "Pulao/Fried Rice": [170, 1.58, 0.037, 0.019, 0.313],
    "Dhalia": [200, 0.91, 0.025, 0.022, 0.153],
    "Plain Parantha": [30, 3.68, 0.090, 0.137, 0.520],
    "Stuffed Parantha": [35, 3.06, 0.077, 0.077, 0.514],
    "Idli": [34, 1.56, 0.059, 0.003, 0.322],
    "Dosa": [42, 2.62, 0.074, 0.068, 0.428],
    "Khichidi": [290, 1.22, 0.031, 0.019, 0.230],
    "Rajma (Curry)": [234, 1.17, 0.055, 0.030, 0.170],
    "Saboot Moong": [200, 0.94, 0.026, 0.054, 0.088],
    "Dhal (Dehusked)": [135, 1.07, 0.033, 0.052, 0.118],
    "Paneer Gravy": [180, 2.21, 0.115, 0.164, 0.068],
    "Green Leafy Veg Curry": [140, 0.92, 0.036, 0.043, 0.097],
    "Mixed Veg Curry": [150, 1.08, 0.021, 0.082, 0.088],
    "Potato/Yam Sabji": [88, 1.25, 0.016, 0.038, 0.210],
    "Ladies finger (Bhindi)": [80, 1.87, 0.042, 0.088, 0.227],
    "Capsicum Sabji": [72, 1.40, 0.019, 0.095, 0.119],
    "Egg Bhurji/Omelette": [46, 2.08, 0.156, 0.156, 0.014],
    "Chicken Gravy": [212, 1.19, 0.144, 0.053, 0.035],
    "Fish Gravy": [168, 1.21, 0.102, 0.071, 0.039],
    "Milk (Full Cream)": [200, 0.67, 0.032, 0.041, 0.044],
    "Curd": [100, 0.67, 0.031, 0.040, 0.043],
    "Tea (with milk/sugar)": [150, 0.64, 0.019, 0.023, 0.089],
    "Banana": [100, 1.16, 0.012, 0.003, 0.272],
    "Apple": [100, 0.60, 0.002, 0.005, 0.134],
    "Mango": [80, 0.46, 0.046, 0.006, 0.169],
}

# --- APP CONFIG ---
st.set_page_config(page_title="Nutrient Calculator", layout="wide")

st.title("🏥 ICMR Clinical Nutrition Tool")
st.info("Calculations based on ICMR-NIN 2024 Guidelines")

# --- STEP 1: PATIENT INFO ---
with st.expander("👤 Patient Identification", expanded=True):
    c1, c2, c3 = st.columns(3)
    cr_no = c1.text_input("CR Number")
    p_name = c2.text_input("Patient Name")
    mobile = c3.text_input("Mobile Number")
    
    a1, a2, a3, a4 = st.columns(4)
    age = a1.number_input("Age (Years)", 1, 110, 30)
    gender = a2.selectbox("Gender", ["Male", "Female"])
    ht = a3.number_input("Height (cm)", 100.0, 220.0, 165.0)
    wt = a4.number_input("Weight (kg)", 10.0, 200.0, 60.0)
    activity = st.select_slider("Activity Level", options=["Sedentary", "Moderate", "Heavy"])

# --- STEP 2: CALCULATE GOALS ---
if gender == "Male":
    bmr = (10 * wt) + (6.25 * ht) - (5 * age) + 5
else:
    bmr = (10 * wt) + (6.25 * ht) - (5 * age) - 161

pal_map = {"Sedentary": 1.2, "Moderate": 1.5, "Heavy": 1.75}
energy_req = round(bmr * pal_map[activity])
protein_req = round(wt * 0.9) # ICMR Average

# --- STEP 3: DIET INTAKE ---
st.header("🥗 Daily Food Intake")
selected_food = st.selectbox("Search Food Item", [""] + list(food_data.keys()))
if selected_food:
    unit_wt = food_data[selected_food][0]
    st.write(f"Standard weight for 1 unit: **{unit_wt}g**")
    qty = st.number_input(f"Number of units of {selected_food}", 0.5, 20.0, 1.0, step=0.5)
    
    if 'diet_list' not in st.session_state:
        st.session_state.diet_list = []
        
    if st.button("Add to Diet Recall"):
        total_g = qty * unit_wt
        st.session_state.diet_list.append({
            "Item": selected_food,
            "Qty": qty,
            "Grams": total_g,
            "kcal": total_g * food_data[selected_food][1],
            "pro": total_g * food_data[selected_food][2],
            "fat": total_g * food_data[selected_food][3],
            "cho": total_g * food_data[selected_food][4]
        })

# --- STEP 4: DISPLAY & RESULTS ---
if 'diet_list' in st.session_state and st.session_state.diet_list:
    df = pd.DataFrame(st.session_state.diet_list)
    st.table(df[["Item", "Qty", "Grams", "kcal", "pro"]])
    
    total_kcal = df["kcal"].sum()
    total_pro = df["pro"].sum()
    
    st.divider()
    res1, res2 = st.columns(2)
    with res1:
        st.metric("Energy Intake", f"{int(total_kcal)} kcal", delta=f"{int(total_kcal - energy_req)} vs Req: {energy_req}")
    with res2:
        st.metric("Protein Intake", f"{int(total_pro)} g", delta=f"{int(total_pro - protein_req)} vs Req: {protein_req}")
    
    if st.button("Clear All"):
        st.session_state.diet_list = []
        st.rerun()