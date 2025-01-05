import streamlit as st
from api_client import add_data, fetch_data

def add_data_ui():
    st.subheader("➕ Add Data")
    data_type = st.selectbox("Select data type to add", ["Elderly", "Caregiver", "Medication"])

    if data_type == "Elderly":
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        if st.button("Add Elderly"):
            payload = {"id": id, "name": name}
            try:
                add_data("elderly", payload)
                st.success(f"Elderly {name} added successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Caregiver":
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        bank_name = st.text_input("Bank Name")
        bank_account = st.text_input("Bank Account")
        branch_number = st.text_input("Branch Number")
        if st.button("Add Caregiver"):
            payload = {
                "id": id,
                "name": name,
                "bank_name": bank_name,
                "bank_account": bank_account,
                "branch_number": branch_number
            }
            try:
                add_data("caregivers", payload)
                st.success(f"Caregiver {name} added successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Medication":
        elderly_id = st.number_input("Elderly ID", min_value=1, step=1)
        name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        frequency = st.text_input("Frequency")
        if st.button("Add Medication"):
            payload = {"name": name, "dosage": dosage, "frequency": frequency}
            try:
                add_data(f"elderly/{elderly_id}/medications", payload)
                st.success(f"Medication {name} added successfully for Elderly ID {elderly_id}!")
            except RuntimeError as e:
                st.error(str(e))
