import streamlit as st
import pandas as pd
import joblib

# Load saved files
model = joblib.load("quality_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("Quality Issues Prediction App")
st.write("Enter the production details below to predict Quality Issues.")

# User input fields
hours_worked = st.number_input("Hours Worked", min_value=0.0, value=38.0)
units_produced = st.number_input("Units Produced", min_value=0.0, value=360.0)
production_cost = st.number_input("Production Cost", min_value=0.0, value=530000.0)
overtime_hours = st.number_input("Overtime Hours", min_value=0.0, value=2.0)
training_hours = st.number_input("Training Hours", min_value=0.0, value=0.0)

rig_location = st.selectbox(
    "Rig Location",
    ["Other / Base Category", "Ekeremor", "Nembe", "Southern Ijaw"]
)

# Prepare input data
input_data = {
    "Hours Worked": hours_worked,
    "Units Produced": units_produced,
    "Production Cost (?)": production_cost,
    "Overtime Hours": overtime_hours,
    "Training Hours": training_hours,
    "Rig Location_Ekeremor": 0,
    "Rig Location_Nembe": 0,
    "Rig Location_Southern Ijaw": 0
}

# Set rig location
if rig_location == "Ekeremor":
    input_data["Rig Location_Ekeremor"] = 1
elif rig_location == "Nembe":
    input_data["Rig Location_Nembe"] = 1
elif rig_location == "Southern Ijaw":
    input_data["Rig Location_Southern Ijaw"] = 1

# Convert to dataframe
input_df = pd.DataFrame([input_data])

# Reorder columns to match training
input_df = input_df[model_columns]

# Make prediction
if st.button("Predict Quality Issues"):
    prediction = model.predict(input_df)[0]

    # Apply business rules
    prediction = max(0, prediction)   # remove negative values
    prediction = round(prediction)    # convert to whole number

    st.success(f"Predicted Quality Issues: {prediction}")