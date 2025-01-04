import streamlit as st
from api_client import fetch_data

def view_data():
    st.subheader("📊 View Data")
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers", "Medications"])

    if st.button("Fetch Data"):
        try:
            # Fetch data from the API
            data = fetch_data(data_type.lower())

            # Format tasks for Elderly data
            if data_type == "Elderly":
                st.write("Elderly:")
                for entry in data:
                    if "tasks" in entry:
                        entry["tasks"] = ", ".join([f"{task['id']}: {task['description']} ({task['status']})" for task in entry["tasks"]])
                    # Display each Elderly as a card
                    with st.expander(f"{entry['name']} (ID: {entry['id']})"):
                        st.markdown(f"**Name:** {entry['name']}")
                        st.markdown(f"**ID:** {entry['id']}")
                        if "tasks" in entry:
                            st.markdown(f"**Tasks:** {entry['tasks']}")

            # Format salary and display Caregivers as cards
            elif data_type == "Caregivers":
                st.write("Caregivers:")
                for caregiver in data:
                    caregiver["id"] = str(caregiver["id"])
                    salary_data = caregiver.get('salary', {})
                    caregiver["salary"] = f"Base: {salary_data.get('price', 'N/A')}, Amount: {salary_data.get('amount', 'N/A')}, Total: {salary_data.get('total', 'N/A')}"
                    # Display each Caregiver as a card
                    with st.expander(f"{caregiver['name']} (ID: {caregiver['id']})"):
                        st.markdown(f"**Bank Name:** {caregiver['bank_name']}")
                        st.markdown(f"**Bank Account:** {caregiver['bank_account']}")
                        st.markdown(f"**Branch Number:** {caregiver['branch_number']}")
                        st.markdown(f"**Salary:** {caregiver['salary']}")

            # Display other data types as a table
            else:
                st.dataframe(data)
        except RuntimeError as e:
            st.error(str(e))

