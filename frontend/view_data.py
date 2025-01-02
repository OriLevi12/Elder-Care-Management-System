import streamlit as st
from api_client import fetch_data

def view_data():
    st.subheader("📊 View Data")
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers", "Medications"])

    if st.button("Fetch Data"):
        try:
            data = fetch_data(data_type.lower())

            if data_type == "Elderly":
                for entry in data:
                    if "tasks" in entry:
                        entry["tasks"] = ", ".join([f"{task['id']}: {task['description']} ({task['status']})" for task in entry["tasks"]])

            if data_type == "Caregivers":
                for entry in data:
                    salary_data = entry.get('salary', {})
                    entry["salary"] = f"Base: {salary_data.get('price', 'N/A')}, Amount: {salary_data.get('amount', 'N/A')}, Total: {salary_data.get('total', 'N/A')}"

            st.dataframe(data)
        except RuntimeError as e:
            st.error(str(e))

