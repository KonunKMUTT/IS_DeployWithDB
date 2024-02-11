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
    input_values = {
        'age': "",
        'impulse': "",
        'pressure_high': "",
        'pressure_low': "",
        'glucose': "",
        'kcm': "",
        'troponin': "",
        'gender': "Female"  # Default value
    }

    # Display input fields
    input_values['age'] = st.text_input("Enter age:", value=input_values['age'])
    input_values['impulse'] = st.text_input("Enter impulse:", value=input_values['impulse'])
    input_values['pressure_high'] = st.text_input("Enter high blood pressure:", value=input_values['pressure_high'])
    input_values['pressure_low'] = st.text_input("Enter low blood pressure:", value=input_values['pressure_low'])
    input_values['glucose'] = st.text_input("Enter glucose level:", value=input_values['glucose'])
    input_values['kcm'] = st.text_input("Enter KCM:", value=input_values['kcm'])
    input_values['troponin'] = st.text_input("Enter troponin level:", value=input_values['troponin'])
    input_values['gender'] = st.selectbox("Select gender", ["Female", "Male"], index=0 if input_values['gender'] == "Female" else 1)

    if st.button("Predict"):
        result = predict_heart_disease(input_values['age'], input_values['impulse'], input_values['pressure_high'], input_values['pressure_low'], input_values['glucose'], input_values['kcm'], input_values['troponin'], 1 if input_values['gender'] == "Female" else 0, 1 if input_values['gender'] == "Male" else 0)
        color = "red" if result == "positive" else "green"
        styled_result = f'<p style="color:{color}; font-size:20px; text-align:center; font-weight:bold; background-color:#4B4A54; padding:10px; border-radius: 15px;">{result}</p>'
        st.markdown(styled_result, unsafe_allow_html=True)

        new_data = pd.DataFrame({
            'age': [input_values['age']],
            'impluse': [input_values['impulse']],
            'pressurehight': [input_values['pressure_high']],
            'pressurelow': [input_values['pressure_low']],
            'glucose': [input_values['glucose']],
            'kcm': [input_values['kcm']],
            'troponin': [input_values['troponin']],
            'female': [1 if input_values['gender'] == "Female" else 0],
            'male': [1 if input_values['gender'] == "Male" else 0],
            'class': [result]
        })

        update_df = pd.concat([ext_data, new_data], ignore_index=True)
        conn.update(worksheet="Sheet1", data=update_df)

        st.success("New Data is Update To GoogleSheets!")

    # Clear button functionality
    if st.button("Clear"):
        # Update input values with empty strings
        for key in input_values:
            input_values[key] = ""

if __name__ == '__main__':
    main()
