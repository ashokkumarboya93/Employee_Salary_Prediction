import streamlit as st
import joblib
import numpy as np

# Set page config
st.set_page_config(
    page_title="💼 Salary Predictor",
    page_icon="💰",
    layout="centered"
)

# Custom Red Theme via inline CSS
st.markdown("""
    <style>
        .main {
            background-color: #ffdddd;
            padding: 2rem;
        }
        html, body, .stApp {
            background-color: #ffdddd;
            color: #222222;
        }
        h1, h2, h3, h4 {
            color: #b30000;
        }
        .stButton>button {
            background-color: #b30000;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: bold;
            font-size: 1rem;
        }
        .stNumberInput>div>div>input {
            border: 1px solid #b30000;
            border-radius: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and info
st.markdown("## 💼 Salary Prediction App")
st.write("Estimate employee salaries based on:")
st.markdown("- ⏳ **Years at the company**")
st.markdown("- ⭐ **Job rating**")

st.divider()

# Input fields
years = st.number_input("🔢 Enter the years at company", value=1, step=1, min_value=0)
job_rate = st.number_input("📊 Enter the job rate (e.g. 3.5)", value=3.5, step=0.5, min_value=0.0)

st.divider()

# Predict button
predict_button = st.button("🚀 Predict Salary")

st.divider()

# Prediction logic
if predict_button:
    try:
        st.balloons()
        X = np.array([years, job_rate]).reshape(1, -1)
        model = joblib.load("model.pkl")
        prediction = model.predict(X)
        st.success(f"✅ Estimated Salary: **₹{prediction[0]:,.2f}**")
    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")
else:
    st.info("ℹ️ Press the button above to generate a prediction.")
