import streamlit as st
import joblib
import numpy as np

st.title("Salary Prediction App")
st.divider()

st.write("With this app, you can get estimations for the salaries of the company employees")

years = st.number_input("Enter the years at company", value=1, step=1, min_value=0)
jobrate = st.number_input("Enter the job rate:", value=3.5, step=0.5, min_value=0.0)

X = [years, jobrate]

try:
    model = joblib.load("model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.divider()
predict = st.button("Press the button for salary prediction")
st.divider()

if predict:
    st.balloons()
    X1 = np.array(X).reshape(1, -1)
    prediction = model.predict(X1)
    st.success(f"Predicted Salary: ₹{prediction[0]:.2f}")
else:
    st.info("Press the button to see the salary prediction")
