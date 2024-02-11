import pickle
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.experimental_connection("gsheets", type=GSheetsConnection)
ext_data = conn.read(worksheet="Sheet1", usecols=list(range(10)), ttl=5)
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

    # Initialize input variables
    age_input = st.text_input("Enter age:")
    impulse_input = st.text_input("Enter impulse:")
    pressure_high_input = st.text_input("Enter high blood pressure:")
    pressure_low_input = st.text_input("Enter low blood pressure:")
    glucose_input = st.text_input("Enter glucose level:")
    kcm_input = st.text_input("Enter KCM:")
    troponin_input = st.text_input("Enter troponin level:")
    gender_input = st.selectbox("Select gender", ["Female", "Male"])

    if gender_input == "Female":
        female = 1
        male = 0
    else:
        female = 0
        male = 1

    if st.button("Predict"):
        result = predict_heart_disease(age_input, impulse_input, pressure_high_input, pressure_low_input, glucose_input, kcm_input, troponin_input, female, male)
        color = "red" if result == "positive" else "green"
        styled_result = f'<p style="color:{color}; font-size:20px; text-align:center; font-weight:bold; background-color:#4B4A54; padding:10px; border-radius: 15px;">{result}</p>'
        st.markdown(styled_result, unsafe_allow_html=True)

        new_data = pd.DataFrame({
            'age': [age_input],
            'impluse': [impulse_input],
            'pressurehight': [pressure_high_input],
            'pressurelow': [pressure_low_input],
            'glucose': [glucose_input],
            'kcm': [kcm_input],
            'troponin': [troponin_input],
            'female': [female],
            'male': [male],
            'class' : [result]
            })

        update_df = pd.concat([ext_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=update_df)

        st.success("New Data is Update To GoogleSheets!")

    # Clear button functionality
    if st.button("Clear"):
        # Update input variables with empty strings
        age_input = ""
        impulse_input = ""
        pressure_high_input = ""
        pressure_low_input = ""
        glucose_input = ""
        kcm_input = ""
        troponin_input = ""
        gender_input = st.selectbox("Select gender", ["Female", "Male"], index=0)

if __name__ == '__main__':
    main()
