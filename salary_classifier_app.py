import streamlit as st
import pandas as pd
import joblib

# ✅ Load Model and Encoders
try:
    model = joblib.load("best_model.pkl")
    occupation_encoder = joblib.load("occupation_encoder.pkl")
    gender_encoder = joblib.load("gender_encoder.pkl")
except FileNotFoundError:
    st.error("Model files not found. Please ensure .pkl files are in the directory.")
    st.stop()

# ✅ Page Config
st.set_page_config(page_title="💸 Employee Salary Predictor", page_icon="💸", layout="wide")

# ✅ Custom Theme Styling
st.markdown("""
<style>
body { background-color: lightblue; color: #0a2540; font-family: 'Segoe UI', sans-serif; }
.stApp { background-color:lightblue; }

/* Input Styling */
.stNumberInput > div > input, .stSelectbox > div > div, .stDataFrame {
    background-color: #ffffff; border: 1px solid #c0c0c0; border-radius: 8px;
}

/* Button Styling */
.stButton > button {
    background-color: #006d77; color: white; font-weight: bold; border-radius: 10px; height: 45px; width: 100%;
    transition: background-color 0.3s ease;
}
.stButton > button:hover { background-color: #004b50; box-shadow: 0 4px 12px rgba(0, 77, 80, 0.3); }
</style>
""", unsafe_allow_html=True)

# ✅ Header with Title & Logo
col_title, col_logo = st.columns([4, 1])

with col_title:
    st.title("💸 Employee Salary Predictor")
    st.markdown("Predict an employee's salary category or range based on key professional metrics.")

with col_logo:
    logo_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwz19Kbw2GnvQvnOTsOLM59pLXX_asnULvDA&s"
    try:
        st.image(logo_url, width=120)
    except Exception:
        st.error("Error loading logo image. Please check the URL or your connection.")

st.markdown("---")

# ✅ Prediction Mode Selector
st.subheader("Choose Prediction Mode 🎯")
mode = st.radio(
    "Select Prediction Type:",
    ["Salary Category (≤50K / >50K)", "Salary Range (₹)", "Both Predictions"],
    horizontal=True
)
st.markdown("---")

# ✅ Input Section
st.subheader("Enter Employee Details 👇")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("👤 Age", min_value=18, max_value=65, value=30)
    gender = st.selectbox("⚧️ Gender", gender_encoder.classes_)
with col2:
    experience = st.number_input("🎓 Education Years", min_value=1, max_value=16, value=9)
    hours = st.number_input("🕒 Hours per Week", min_value=1, max_value=80, value=40)
with col3:
    occupation = st.selectbox("💼 Occupation", occupation_encoder.classes_)

# ✅ Input Encoding
occupation_encoded = occupation_encoder.transform([occupation])[0]
gender_encoded = gender_encoder.transform([gender])[0]

input_df = pd.DataFrame({
    'age': [age],
    'experience': [experience],
    'occupation': [occupation_encoded],
    'hours-per-week': [hours],
    'gender': [gender_encoded]
})

st.markdown("---")
st.subheader("Your Entered Details 📄")
st.dataframe(input_df, use_container_width=True)

# ✅ Gradient Result Block Function
def show_result(message, color1, color2):
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color1}, {color2});
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        text-align: center;
        color: #ffffff;
        font-size: 22px;
        font-weight: 600;">
        {message}
    </div>
    """, unsafe_allow_html=True)

# ✅ Predict Button Logic
if st.button("🚀 Predict Salary"):
    with st.spinner("Analyzing Data..."):
        pred = model.predict(input_df)[0]

        if mode == "Salary Category (≤50K / >50K)":
            category = ">50K 💰" if pred == 1 else "≤50K 💼"
            colors = ("#0f2027", "#2c5364") if pred == 1 else ("#c31432", "#240b36")
            show_result(f"🎯 Predicted Category: {category}", colors[0], colors[1])

        elif mode == "Salary Range (₹)":
            salary_ranges = {
                0: "₹15,000 - ₹30,000",
                1: "₹30,001 - ₹50,000",
                2: "₹50,001 - ₹70,000",
                3: "₹70,001 - ₹1,00,000",
                4: "₹1,00,000+"
            }
            range_label = salary_ranges.get(pred, "Unknown ❓")
            show_result(f"📊 Predicted Range: {range_label}", "#fc4a1a", "#f7b733")

        else:
            category = ">=50K 💰" if pred == 1 else "≤50K 💼"
            salary_ranges = {
                0: "₹15,000 - ₹30,000",
                1: "₹30,001 - ₹50,000",
                2: "₹50,001 - ₹70,000",
                3: "₹70,001 - ₹1,00,000",
                4: "₹1,00,000+"
            }
            range_label = salary_ranges.get(pred, "Unknown ❓")
            show_result(f"🎯 Category: {category}", "#0f2027", "#2c5364")
            show_result(f"📊 Range: {range_label}", "#fc4a1a", "#f7b733")
