import streamlit as st
import requests

# Backend API base URL
API_BASE_URL = "http://backend:8000"

st.title("Elder Care Management System")

# Sidebar Navigation
menu = ["View Data", "Add Data"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Data":
    st.subheader("View Data")
    
    # Choose the type of data to view
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers", "Medications"])
    
    if st.button("Fetch Data"):
        try:
            response = requests.get(f"{API_BASE_URL}/{data_type.lower()}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            st.error(f"Connection error: {e}")

elif choice == "Add Data":
    st.subheader("Add Data")
    
    # Choose the type of data to add
    data_type = st.selectbox("Select data type to add", ["Elderly", "Caregiver", "Task", "Medication"])
    
    if data_type == "Elderly":
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        
        if st.button("Add Elderly"):
            payload = {"id": id, "name": name}
            try:
                response = requests.post(f"{API_BASE_URL}/elderly", json=payload)
                if response.status_code == 200:
                    st.success("Elderly added successfully!")
                else:
                    st.error(f"Error adding elderly: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
    
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
                response = requests.post(f"{API_BASE_URL}/caregivers", json=payload)
                if response.status_code == 200:
                    st.success("Caregiver added successfully!")
                else:
                    st.error(f"Error adding caregiver: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")

    elif data_type == "Task":
        elderly_id = st.number_input("Elderly ID", min_value=1, step=1)
        description = st.text_input("Task Description")
        status = st.text_input("Task Status", value="pending", help="Enter task status (e.g., 'pending', 'completed').")
        
        if st.button("Add Task"):
            payload = {
                "description": description,
                "status": status
            }
            try:
                response = requests.post(f"{API_BASE_URL}/elderly/{elderly_id}/tasks", json=payload)
                if response.status_code == 200:
                    st.success("Task added successfully!")
                else:
                    st.error(f"Error adding task: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")

    elif data_type == "Medication":
        name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        frequency = st.text_input("Frequency")
        
        if st.button("Add Medication"):
            payload = {"name": name, "dosage": dosage, "frequency": frequency}
            try:
                response = requests.post(f"{API_BASE_URL}/medications", json=payload)
                if response.status_code == 200:
                    st.success("Medication added successfully!")
                else:
                    st.error(f"Error adding medication: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")

