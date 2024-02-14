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

    age = st.text_input("Enter age:")
    impulse = st.text_input("Enter impulse:")
    pressure_high = st.text_input("Enter high blood pressure:")
    pressure_low = st.text_input("Enter low blood pressure:")
    glucose = st.text_input("Enter glucose level:")
    kcm = st.text_input("Enter KCM:")
    troponin = st.text_input("Enter troponin level:")
    gender = st.selectbox("Select gender", ["Female", "Male"])

    # Set gender value based on selection
    if gender == "Female":
        female = 1
        male = 0
    else:
        female = 0
        male = 1
           
    if st.button("Predict"):
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
        'class' : [result]
        })

        update_df = pd.concat([ext_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=update_df)

        st.success("New Data is Update To GoogleSheets!")
        
if __name__ == '__main__':
    main()

if st.toggle("Show Distribution by Gender"):
        # Change 0 as "Male" and 1 as "Female"
        ext_data["female"] = ext_data["female"].replace({0: "Male", 1: "Female"})

        # Calculate %
        total_female = ext_data[ext_data["female"] == "Female"].shape[0]
        total_male = ext_data[ext_data["female"] == "Male"].shape[0]
        ext_data["Female %"] = (ext_data["female"] == "Female") * (100 / total_female)
        ext_data["Male %"] = (ext_data["female"] == "Male") * (100 / total_male)

        # Create Graph Count Plot
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.countplot(y="female", hue="class", data=ext_data, ax=ax)

        # Change labels name
        ax.set_ylabel("Gender")

        # Shown Graph
        st.pyplot(fig)
