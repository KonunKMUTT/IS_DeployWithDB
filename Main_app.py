import pickle
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

conn = st.connection("gsheets", type=GSheetsConnection)
ext_data = conn.read(wroksheet="Sheet1", usecols=list(range(10)), ttl=5)
ext_data = ext_data.dropna(how="all")

# Load the model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Function to make prediction
def predict_heart_disease(age, impulse, pressure_high, pressure_low, glucose, kcm, troponin, female, male):
    x_new = pd.DataFrame({
        'age': [age],
        'impluse': [impulse],
        'pressurehight': [pressure_high],
        'pressurelow': [pressure_low],
        'glucose': [glucose],
        'kcm': [kcm],
        'troponin': [troponin],
        'female': [female],
        'male': [male]
        })

    y_pred_new = model.predict(x_new)
    return y_pred_new[0].strip()

# Streamlit app
def main():
    st.markdown('<p style="text-align:center; font-weight:bold; font-size:30px;">Heart Disease Prediction App</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;">Enter the data to prediction, Please Ensure all feilds are filled.</p>', unsafe_allow_html=True)

    age = st.text_input("Enter age: (Age range 0 to 150)", 0, 150)
    impulse = st.slider("Enter impulse: (Impulse range 10 to 200)", 10, 200)
    pressure_high = st.slider("Enter high blood pressure: (High blood pressure range 70 to 200)", 70, 200)
    pressure_low = st.slider("Enter low blood pressure: (High blood pressure range 40 to 120)", 40, 120)
    glucose = st.text_input("Enter glucose level: (Glucose range 1 to 900)", 1, 900)
    kcm = st.number_input("Enter CK-MB (KCM): (CK-MB range 0.00 to 10.00)", 0.00, 10.00)
    troponin = st.number_input("Enter troponin level: (Troponin range 0.000 to 0.040)", 0.000, 0.040, 0.001, float)
    gender = st.selectbox("Select gender", ["Female", "Male"])

    # Set gender value based on selection
    if gender == "Female":
        female = 1
        male = 0
    else:
        female = 0
        male = 1
    
    if st.button("Predict"):
        if not age or not impulse or not pressure_high or not pressure_low or not glucose or not kcm or not troponin:
            st.warning("Please Ensure all feilds are filled.")
            st.stop()
        else:
            result = predict_heart_disease(age, impulse, pressure_high, pressure_low, glucose, kcm, troponin, female, male)

            # Set color based on the result
            color = "red" if result == "positive" else "green"  # Adjust this condition based on your model's output
    
            # Apply styling with HTML
            styled_result = f'<p style="color:{color}; font-size:20px; text-align:center; font-weight:bold; background-color:#4B4A54; padding:10px; border-radius: 15px;">{result}</p>'
    
            # Display the styled result
            st.markdown(styled_result, unsafe_allow_html=True)

            new_data = pd.DataFrame({
                'age': [age],
                'impluse': [impulse],
                'pressurehight': [pressure_high],
                'pressurelow': [pressure_low],
                'glucose': [glucose],
                'kcm': [kcm],
                'troponin': [troponin],
                'female': [female],
                'male': [male],
                'class': [result]
                })

            update_df = pd.concat([ext_data, new_data], ignore_index=True)
            conn.update(worksheet="Sheet1", data=update_df)
    
            st.success("New Data is Update To GoogleSheets!")
        
if __name__ == '__main__':
    main()

if st.toggle("Show Distribution By Gender"):
  
    # เปลี่ยน 0 เป็น "Male" และ 1 เป็น "Female"
    ext_data["female"] = ext_data["female"].replace({0: "Male", 1: "Female"})

    # Create countplot
    fig, ax = plt.subplots(figsize=(4, 4))
    sns.countplot(x="female", hue="class", data=ext_data, ax=ax)

    # Display Plotly figure in Streamlit
    st.pyplot(fig)

if st.toggle("Show Distribution By Age"):

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(data=ext_data, x="age", hue="class")
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(4, 2))
    sns.boxplot(data=ext_data, x="age", y="class")
    st.pyplot(fig)
