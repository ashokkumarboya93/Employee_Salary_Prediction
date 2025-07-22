import streamlit as st
import pandas as pd
import joblib

# ✅ Load Model and Encoders
try:
    model = joblib.load("best_model.pkl")
except FileNotFoundError:
    st.error("Model file not found. Please ensure 'best_model.pkl' is in the directory.")
    st.stop()

# ✅ Page Configuration
st.set_page_config(page_title="💼 Employee Salary Predictor", page_icon="💼", layout="wide")

# ✅ Styling
st.markdown("""
<style>
body { background: linear-gradient(to right, #ffecd2, #fcb69f); font-family: 'Segoe UI', sans-serif; }
.stApp { background: linear-gradient(to right, #ffecd2, #fcb69f); }
.stButton > button {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}
.stButton > button:hover { background: linear-gradient(to right, #2c5364, #203a43, #0f2027); }
</style>
""", unsafe_allow_html=True)

# ✅ Title and Description
st.title("💼 Employee Salary Predictor")
st.markdown("Predict employee salary category using demographic and professional attributes.")
st.markdown("---")

# ✅ Sidebar Input Section
st.sidebar.header("Enter Employee Details")

# ✅ Age Input
age = st.sidebar.number_input("Age", min_value=18, max_value=65, value=30)

# ✅ Gender Input (manual)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
gender_encoded = 1 if gender == "Male" else 0

# ✅ Occupation Input (manual job roles)
occupation_list = [
    "Machine-op-inspct",
    "Farming-fishing",
    "Protective-serv",
    "Other-service",
    "Prof-specialty"
]
occupation = st.sidebar.selectbox("Occupation", occupation_list)

# ✅ Simple Encoding for Occupation (mapping job roles)
occupation_mapping = {
    "Machine-op-inspct": 0,
    "Farming-fishing": 1,
    "Protective-serv": 2,
    "Other-service": 3,
    "Prof-specialty": 4
}
occupation_encoded = occupation_mapping[occupation]

# ✅ Experience & Hours Inputs
experience = st.sidebar.number_input("Education Years", min_value=1, max_value=16, value=9)
hours = st.sidebar.number_input("Hours-per-Week", min_value=1, max_value=80, value=40)

# ✅ Create Input DataFrame
input_df = pd.DataFrame({
    'age': [age],
    'experience': [experience],
    'occupation': [occupation_encoded],
    'hours-per-week': [hours],
    'gender': [gender_encoded]
})

st.markdown("---")
st.subheader("Entered Details 📄")
st.dataframe(input_df, use_container_width=True)

# ✅ Result Display Block
def show_result(message, color1, color2):
    st.markdown(f"""
    <div style="
        background: linear-gradient(to right, {color1}, {color2});
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;">
        {message}
    </div>
    """, unsafe_allow_html=True)

# ✅ Prediction Button
if st.button("🚀 Predict Salary Category"):
    with st.spinner("Predicting..."):
        pred = model.predict(input_df)[0]
        category = ">50K 💰" if pred == 1 else "≤50K 💼"
        colors = ("#11998e", "#38ef7d") if pred == 1 else ("#f85032", "#e73827")
        show_result(f"🎯 Predicted Salary Category: {category}", colors[0], colors[1])
