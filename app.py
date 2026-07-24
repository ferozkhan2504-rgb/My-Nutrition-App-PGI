import streamlit as st
import pandas as pd
from datetime import datetime

# --- FULL FOOD & LIQUID DATABASE (143+ Items) ---
# Format: "Item": ["Unit", GramsPerUnit, Energy, Protein, Fat, Carbs, Chol, Fibre, SFA, MUFA, PUFA]
food_master = {
    "Chapati with ghee": ["No.", 25, 4.41, 0.138, 0.076, 0.793, 0.16, 0.021, 0.041, 0.056, 0.024],
    "Chapati dry": ["No.", 25, 3.90, 0.138, 0.019, 0.793, 0.00, 0.021, 0.003, 0.014, 0.009],
    "Bread, toast, rolls, buns": ["No.", 15, 2.45, 0.078, 0.007, 0.519, 0.00, 0.002, 0.001, 0.005, 0.003],
    "Cornflakes": ["Katori", 108, 1.61, 0.037, 0.030, 0.296, 0.00, 0.006, 0.003, 0.008, 0.007],
    "Pulao / fried rice / zeera rice": ["Katori", 170, 1.58, 0.037, 0.019, 0.313, 0.00, 0.012, 0.002, 0.010, 0.004],
    "Boiled Rice": ["Katori", 150, 0.99, 0.019, 0.001, 0.225, 0.00, 0.040, 0.000, 0.000, 0.000],
    "Dhalia, all types": ["Katori", 200, 0.91, 0.025, 0.022, 0.153, 0.00, 0.005, 0.002, 0.005, 0.004],
    "Plain Paranth": ["No.", 30, 3.68, 0.090, 0.137, 0.520, 0.00, 0.014, 0.016, 0.075, 0.031],
    "Stuffed Parantha": ["No.", 35, 3.06, 0.077, 0.077, 0.514, 0.00, 0.016, 0.009, 0.040, 0.018],
    "Porridge": ["Katori", 100, 1.08, 0.021, 0.012, 0.221, 0.00, 0.002, 0.001, 0.005, 0.003],
    "Rusk": ["No.", 25, 5.43, 0.122, 0.070, 1.077, 0.00, 0.008, 0.003, 0.005, 0.002],
    "puri bhatura": ["No.", 20, 3.45, 0.073, 0.162, 0.423, 0.00, 0.011, 0.001, 0.010, 0.006],
    "Uppama": ["Katori", 200, 2.64, 0.040, 0.169, 0.241, 0.00, 0.019, 0.009, 0.062, 0.037],
    "Poha": ["Katori", 154, 2.79, 0.060, 0.101, 0.408, 0.00, 0.013, 0.004, 0.028, 0.025],
    "Noodles, pasta, macaroni": ["Katori", 166, 1.08, 0.014, 0.002, 0.252, 0.00, 0.008, 0.000, 0.000, 0.000],
    "Pizza, Burger etc.": ["No.", 76, 2.95, 0.160, 0.067, 0.428, 0.03, 0.000, 0.005, 0.017, 0.007],
    "Dosa": ["No.", 42, 2.62, 0.074, 0.068, 0.428, 0.00, 0.002, 0.000, 0.001, 0.001],
    "Idli": ["No.", 34, 1.56, 0.059, 0.003, 0.322, 0.00, 0.042, 0.000, 0.000, 0.000],
    "Khichidi": ["Katori", 290, 1.22, 0.031, 0.019, 0.230, 0.00, 0.001, 0.002, 0.006, 0.004],
    "Rajma": ["Katori", 234, 1.17, 0.055, 0.030, 0.170, 0.00, 0.016, 0.003, 0.007, 0.005],
    "Saboot Moong": ["Katori", 200, 0.94, 0.026, 0.054, 0.088, 0.00, 0.005, 0.003, 0.006, 0.004],
    "Other whole gram curries": ["Katori", 234, 0.78, 0.019, 0.044, 0.077, 0.00, 0.006, 0.002, 0.005, 0.002],
    "Dehusked dhal, all types": ["Katori", 135, 1.07, 0.033, 0.052, 0.118, 0.00, 0.005, 0.002, 0.006, 0.002],
    "Dhals with husk, all types": ["Katori", 150, 0.76, 0.030, 0.028, 0.097, 0.00, 0.011, 0.003, 0.006, 0.004],
    "Buttermilk curry": ["Katori", 220, 0.52, 0.028, 0.013, 0.071, 0.02, 0.118, 0.007, 0.002, 0.003],
    "Kofta curry": ["Katori", 185, 1.91, 0.031, 0.147, 0.117, 0.03, 0.018, 0.011, 0.039, 0.017],
    "Green leafy vegetable curries": ["Katori", 140, 0.92, 0.036, 0.043, 0.097, 0.00, 0.011, 0.004, 0.014, 0.007],
    "Paneer gravy": ["Katori", 180, 2.21, 0.115, 0.164, 0.068, 0.08, 0.009, 0.080, 0.037, 0.004],
    "Mint / coriander chutney": ["Tbsp", 5, 0.50, 0.016, 0.004, 0.101, 0.00, 0.015, 0.000, 0.000, 0.000],
    "Tomato, tamrind, other chutneys": ["Tbsp", 5, 0.40, 0.011, 0.001, 0.087, 0.00, 0.008, 0.000, 0.000, 0.000],
    "Veg/ Non veg soup": ["Katori", 180, 0.59, 0.014, 0.046, 0.028, 0.13, 0.079, 0.012, 0.046, 0.028],
    "Salad with raw vegetables": ["Tbsp", 25, 0.36, 0.010, 0.002, 0.074, 0.00, 0.007, 0.000, 0.000, 0.000],
    "salad with sprouted grams": ["Tbsp", 25, 0.87, 0.038, 0.010, 0.156, 0.00, 0.012, 0.004, 0.001, 0.002],
    "Papad Roasted": ["No.", 10, 2.26, 0.175, 0.010, 0.391, 0.00, 0.030, 0.000, 0.000, 0.000],
    "Papad Fried": ["No.", 12, 3.78, 0.175, 0.169, 0.391, 0.00, 0.030, 0.057, 0.078, 0.017],
    "Pickle": ["Tsp.", 6, 2.50, 0.056, 0.199, 0.119, 0.00, 0.042, 0.011, 0.053, 0.111],
    "Boiled egg, bhurji, omlette": ["No.", 46, 2.08, 0.156, 0.156, 0.014, 4.98, 0.000, 0.048, 0.059, 0.021],
    "Egg gravy": ["Katori", 208, 1.04, 0.068, 0.064, 0.047, 2.02, 0.268, 0.014, 0.024, 0.018],
    "Chicken Gravy": ["Katori", 212, 1.19, 0.144, 0.053, 0.035, 0.37, 0.064, 0.006, 0.029, 0.011],
    "Chicken fried / roasted etc.": ["No.", 150, 1.73, 0.271, 0.058, 0.030, 0.74, 0.005, 0.015, 0.025, 0.011],
    "Mutton, pork, beef curries.": ["Katori", 150, 1.47, 0.084, 0.109, 0.037, 0.30, 0.034, 0.031, 0.054, 0.021],
    "Fish gravy": ["Katori", 168, 1.21, 0.102, 0.071, 0.039, 0.36, 0.887, 0.012, 0.026, 0.015],
    "Fish fried.": ["No.", 100, 3.63, 0.179, 0.314, 0.021, 0.65, 1.664, 0.042, 0.180, 0.065],
    "Ham, salami, bacon etc.": ["No.", 50, 2.57, 0.150, 0.206, 0.028, 0.65, 0.150, 0.047, 0.094, 0.082],
    "Bhel Puri, other chats": ["Katori", 110, 1.44, 0.038, 0.053, 0.202, 0.00, 0.006, 0.001, 0.004, 0.002],
    "Patties": ["No.", 120, 6.03, 0.108, 0.278, 0.774, 0.00, 0.168, 0.000, 0.007, 0.016],
    "Pakoda, samosas, mathies.etc.": ["No.", 50, 6.84, 0.074, 0.507, 0.494, 0.00, 0.057, 0.004, 0.023, 0.011],
    "Biscuits, salted": ["No.", 10, 4.48, 0.132, 0.044, 0.890, 0.02, 0.023, 0.001, 0.008, 0.007],
    "Biscuits sweet, cream etc.": ["No.", 15, 4.53, 0.079, 0.102, 0.822, 0.06, 0.064, 0.001, 0.023, 0.004],
    "Namkeen, mixture etc.": ["Tbsp", 20, 6.89, 0.126, 0.595, 0.257, 0.06, 0.063, 0.038, 0.138, 0.137],
    "Chips, Khichre etc.": ["Katori", 30, 3.22, 0.017, 0.243, 0.243, 0.02, 0.028, 0.003, 0.009, 0.002],
    "Groundnuts, cashew nuts etc.": ["Tbsp", 20, 6.78, 0.271, 0.507, 0.282, 0.08, 0.086, 0.000, 0.000, 0.003],
    "Ice cream": ["Katori", 108, 2.05, 0.031, 0.110, 0.236, 0.06, 0.067, 0.003, 0.002, 0.002],
    "Cakes / pastries": ["No.", 50, 4.71, 0.070, 0.270, 0.500, 0.15, 0.155, 0.008, 0.069, 0.030],
    "Custard, Kheer": ["Katori", 200, 2.22, 0.061, 0.068, 0.342, 0.03, 0.038, 0.012, 0.011, 0.001],
    "Gulab Jamun, jalebi etc.": ["No.", 30, 3.88, 0.089, 0.218, 0.390, 0.07, 0.077, 0.003, 0.001, 0.001],
    "Rasgulla, rasmalai etc.": ["No.", 40, 3.78, 0.144, 0.184, 0.387, 0.11, 0.306, 0.005, 0.003, 0.002],
    "Sweet Mathi, malpuda, toshi etc.": ["No.", 35, 6.46, 0.061, 0.466, 0.507, 0.12, 0.129, 0.004, 0.012, 0.003],
    "Halwa": ["Tbsp", 60, 3.21, 0.029, 0.206, 0.309, 0.02, 0.023, 0.002, 0.008, 0.002],
    "Ladoo/ Pinni": ["No.", 56, 5.19, 0.056, 0.266, 0.641, 0.16, 0.166, 0.000, 0.001, 0.000],
    "Chocolates": ["No.", 25, 5.55, 0.072, 0.328, 0.579, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Candies": ["No.", 10, 5.07, 0.064, 0.278, 0.580, 0.10, 0.108, 0.001, 0.009, 0.001],
    "Milk": ["Glass", 200, 0.67, 0.032, 0.041, 0.044, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Flavoured milk": ["Glass", 200, 0.94, 0.037, 0.041, 0.104, 0.02, 0.024, 0.001, 0.010, 0.004],
    "Tea": ["Glass", 150, 0.64, 0.019, 0.023, 0.089, 0.07, 0.085, 0.014, 0.006, 0.000],
    "Coffee": ["Glass", 150, 0.81, 0.030, 0.037, 0.088, 0.02, 0.023, 0.001, 0.009, 0.001],
    "Curd": ["Katori", 100, 0.67, 0.031, 0.040, 0.043, 0.13, 0.000, 0.025, 0.011, 0.001],
    "Raitha with boondi": ["Katori", 200, 0.79, 0.035, 0.051, 0.047, 0.02, 0.179, 0.001, 0.005, 0.000],
    "Raitha with vegetables": ["Katori", 200, 0.61, 0.027, 0.030, 0.057, 0.01, 0.127, 0.000, 0.001, 0.000],
    "Sweet lassi": ["Glass", 250, 0.35, 0.010, 0.014, 0.045, 0.00, 0.009, 0.000, 0.001, 0.000],
    "Namkeen lassi": ["Glass", 250, 0.10, 0.005, 0.007, 0.005, 0.00, 0.004, 0.000, 0.000, 0.000],
    "Fresh fruit juices": ["Glass", 200, 1.13, 0.013, 0.005, 0.258, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Fanta, pepsi etc.": ["Glass", 250, 0.41, 0.000, 0.000, 0.104, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Whisky": ["30 ml", 30, 0.00, 0.000, 0.000, 0.000, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Beer": ["Glass", 200, 0.16, 0.003, 0.000, 0.037, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Wine": ["Glass", 200, 0.06, 0.002, 0.000, 0.014, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Cheese": ["Cubes", 24, 3.47, 0.241, 0.251, 0.063, 0.15, 0.157, 0.008, 0.069, 0.028],
    "Butter / Cream": ["Tsp", 6, 7.32, 0.008, 0.810, 0.000, 2.18, 0.000, 0.504, 0.212, 0.018],
    "Ghee": ["Tsp", 5, 9.00, 0.000, 1.000, 0.000, 2.80, 0.000, 0.675, 0.250, 0.020],
    "Tomato Sauce": ["Tsp", 12, 0.35, 0.013, 0.001, 0.071, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Added salt": ["Pinch", 0.5, 0.00, 0.000, 0.000, 0.000, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Added sugar": ["Tsp", 5, 3.98, 0.001, 0.000, 0.994, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Jam": ["Tsp", 5, 2.77, 0.003, 0.000, 0.688, 0.03, 0.000, 0.000, 0.000, 0.000],
    "Jaggery": ["Tsp", 7, 3.82, 0.004, 0.001, 0.950, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Banana": ["No.", 100, 1.16, 0.012, 0.003, 0.272, 0.00, 0.004, 0.001, 0.000, 0.000],
    "Mango (S=3.5)": ["No.", 80, 0.57, 0.046, 0.006, 0.169, 0.00, 0.012, 0.000, 0.001, 0.000],
    "Apple": ["No.", 100, 0.60, 0.002, 0.005, 0.134, 0.00, 0.010, 0.000, 0.000, 0.001],
    "Water melon (S=7)": ["Slice", 100, 0.33, 0.070, 0.003, 0.035, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Peaches": ["No.", 50, 0.49, 0.012, 0.003, 0.105, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Pears": ["No.", 90, 0.51, 0.006, 0.002, 0.119, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Orange (S=4)": ["No.", 100, 0.48, 0.022, 0.002, 0.109, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Gauva": ["No.", 55, 0.51, 0.009, 0.003, 0.112, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Papaya": ["Slice", 80, 0.51, 0.009, 0.003, 0.112, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Plum (S=3)": ["No.", 25, 0.51, 0.007, 0.005, 0.111, 0.05, 0.000, 0.000, 0.000, 0.000],
    "Grapes": ["Katori", 152, 0.58, 0.006, 0.004, 0.131, 0.01, 0.001, 0.000, 0.000, 0.000],
    "Musambi": ["No.", 110, 0.43, 0.008, 0.003, 0.093, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Pineapple": ["Slice", 52, 0.45, 0.004, 0.001, 0.108, 0.02, 0.000, 0.000, 0.000, 0.000],
    "Pomegranet": ["No.", 144, 0.65, 0.016, 0.001, 0.145, 0.04, 0.001, 0.000, 0.000, 0.000],
    "Zizyphus (S=3)": ["No.", 10, 0.73, 0.008, 0.003, 0.170, 0.00, 0.000, 0.000, 0.000, 0.000],
    "Ghia, tori, Karela": ["Tbsp", 140, 0.95, 0.015, 0.059, 0.089, 0.03, 0.034, 0.000, 0.000, 0.000],
    "Ladies finger (Bhindi)": ["Tbsp", 80, 1.87, 0.042, 0.088, 0.227, 0.00, 0.010, 0.005, 0.004, 0.005],
    "Potato, Yam": ["Tbsp", 88, 1.25, 0.016, 0.038, 0.210, 0.00, 0.004, 0.000, 0.014, 0.005],
    "Capsicum": ["Tbsp", 72, 1.40, 0.019, 0.095, 0.119, 0.01, 0.011, 0.001, 0.034, 0.013],
    "Tinda (S=4)": ["Tbsp", 160, 1.18, 0.022, 0.082, 0.088, 0.00, 0.009, 0.000, 0.000, 0.000],
    "Green leafy vegetables": ["Tbsp", 88, 0.92, 0.036, 0.043, 0.097, 0.00, 0.011, 0.004, 0.014, 0.007],
    "Cabbage": ["Tbsp", 80, 0.98, 0.024, 0.044, 0.122, 0.00, 0.005, 0.002, 0.000, 0.002],
    "Cauliflower": ["Tbsp", 136, 1.14, 0.031, 0.051, 0.139, 0.00, 0.006, 0.002, 0.001, 0.003],
    "Brinjal": ["Tbsp", 80, 1.08, 0.015, 0.081, 0.073, 0.00, 0.009, 0.001, 0.001, 0.004],
    "Drumstick": ["Tbsp", 140, 1.08, 0.021, 0.082, 0.064, 0.00, 0.009, 0.000, 0.000, 0.000],
    "Colocasia": ["Tbsp", 140, 2.03, 0.039, 0.096, 0.253, 0.01, 0.011, 0.000, 0.000, 0.000],
    "Fresh peas": ["Tbsp", 88, 0.56, 0.031, 0.013, 0.080, 0.00, 0.001, 0.000, 0.000, 0.000],
    "Kathal": ["Tbsp", 140, 1.54, 0.022, 0.119, 0.094, 0.01, 0.014, 0.000, 0.000, 0.000],
    "Beans": ["Tbsp", 100, 1.13, 0.024, 0.052, 0.139, 0.00, 0.006, 0.003, 0.007, 0.006],
}

# --- PAGE CONFIG ---
st.set_page_config(page_title="PGI Nutrition Tool", layout="wide")

# --- UI SETUP ---
st.title("🏥 Patient Nutrition & IPAQ Assessment")
st.caption("Simplified version without PDF library dependencies.")

# 1. Demographics
with st.expander("👤 Patient Details", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    cr_no = c1.text_input("CR Number")
    p_name = c2.text_input("Name")
    mobile = c3.text_input("Mobile")
    age = c4.number_input("Age", 1, 100, 30)
    
    c5, c6, c7 = st.columns(3)
    ht = c5.number_input("Height (cm)", 100.0, 220.0, 165.0)
    wt = c6.number_input("Weight (kg)", 10.0, 200.0, 60.0)
    gender = c7.selectbox("Gender", ["Male", "Female"])

# 2. IPAQ (7 Questions)
st.markdown("---")
st.header("🚶 Physical Activity (IPAQ)")
ci1, ci2 = st.columns(2)
with ci1:
    v_d = st.number_input("1. Vigorous activity days per week", 0, 7)
    v_m = st.number_input("2. Minutes spent on vigorous activity per day", 0, 480)
    m_d = st.number_input("3. Moderate activity days per week", 0, 7)
    m_m = st.number_input("4. Minutes spent on moderate activity per day", 0, 480)
with ci2:
    w_d = st.number_input("5. Walking days per week", 0, 7)
    w_m = st.number_input("6. Minutes spent walking per day", 0, 480)
    s_m = st.number_input("7. Minutes spent sitting per weekday", 0, 1440, 300)

# Calculate MET
met_score = (v_d * v_m * 8.0) + (m_d * m_m * 4.0) + (w_d * w_m * 3.3)
pal = 1.75 if met_score >= 3000 else (1.5 if met_score >= 600 else 1.2)
act_cat = "Active" if pal==1.75 else "Moderate" if pal==1.5 else "Sedentary"

# 3. FFQ (Vertical List)
st.markdown("---")
st.header("🥗 Diet Recall (FFQ)")
st.info("Expand each category to fill frequency and portion.")
ffq_res = {}
for food, meta in food_master.items():
    with st.expander(f"🍴 {food} ({meta[0]})"):
        f1, f2, f3 = st.columns(3)
        freq = f1.number_input(f"Frequency value", 0.0, 100.0, 0.0, key=f"f_{food}")
        per = f2.selectbox(f"Period", ["Day", "Week", "Month", "Never"], key=f"p_{food}")
        qty = f3.number_input(f"Portion Size", 0.0, 20.0, 1.0, key=f"q_{food}")
        ffq_res[food] = {"f": freq, "p": per, "q": qty}

# 4. Results
if st.button("🏁 GENERATE REPORT"):
    bmi = round(wt / ((ht/100)**2), 1)
    
    # Nutrient sums [Energy, Protein, Fat, Carbs, Chol, Fibre, SFA, MUFA, PUFA]
    totals = [0.0] * 9
    for item, d in ffq_res.items():
        if d["p"] == "Never" or d["f"] == 0: continue
        m = {"Day": 1, "Week": 1/7, "Month": 1/30}[d["p"]]
        daily_g = d["f"] * m * d["q"] * food_master[item][1]
        for i in range(9): totals[i] += daily_g * food_master[item][i+2]

    # Requirements logic
    bmr = (10 * wt) + (6.25 * ht) - (5 * age) + (5 if gender == "Male" else -161)
    e_req = round(bmr * pal)
    reqs = [e_req, round(wt*0.9), round((e_req*0.25)/9), round((e_req*0.6)/4), 200, 30, 15, 20, 15]
    labels = ["Energy (kcal)", "Protein (g)", "Fats (g)", "Carbs (g)", "Cholesterol (mg)", "Fibre (g)", "SFA (g)", "MUFA (g)", "PUFA (g)"]

    # --- DISPLAY FINAL ANALYSIS ---
    st.markdown("---")
    st.header("📊 Final Clinical Analysis")
    
    r1, r2, r3 = st.columns(3)
    r1.metric("BMI Status", f"{bmi}", "Normal" if 18.5 < bmi < 25 else "Check")
    r2.metric("Total MET-min/week", int(met_score))
    r3.metric("Activity Category", act_cat)

    # Comparison Table
    res_df = pd.DataFrame({
        "Nutrient": labels, 
        "Requirement (R)": reqs, 
        "Actual Intake (In)": [round(x,1) for x in totals]
    })
    res_df["Difference"] = res_df["Actual Intake (In)"] - res_df["Requirement (R)"]
    st.table(res_df)

    # Excel Download
    db_entry = {"Date": datetime.now().strftime("%Y-%m-%d"), "CR_No": cr_no, "Name": p_name, "BMI": bmi, "MET": met_score}
    for i, l in enumerate(labels): db_entry[l] = round(totals[i], 1)
    csv = pd.DataFrame([db_entry]).to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download Patient Data (Excel/CSV)", csv, f"Data_{cr_no}.csv", "text/csv")
    
    st.success("You can now take a screenshot of the results above to share.")
