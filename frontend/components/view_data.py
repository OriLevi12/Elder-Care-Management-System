import streamlit as st
from api_client import fetch_data

def view_data():
    st.subheader("📊 View Data")
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers"])

    if st.button("Fetch Data"):
        try:
            # Fetch data from the API
            data = fetch_data(data_type.lower())

            # Display Elderly data with tasks and medications
            if data_type == "Elderly":
                st.write("Elderly:")
                for entry in data:
                    with st.expander(f"{entry['name']} (ID: {entry['id']})"):
                        st.markdown(f"**Name:** {entry['name']}")
                        st.markdown(f"**ID:** {entry['id']}")
                        st.markdown("**Tasks:**")
                        for task in entry.get("tasks", []):
                            st.write(f"- {task['description']} ({task['status']})")
                        st.markdown("**Medications:**")
                        for med in entry.get("medications", []):
                            st.write(f"- {med['name']} ({med['dosage']}, {med['frequency']})")

            # Display Caregiver data
            elif data_type == "Caregivers":
                st.write("Caregivers:")
                for caregiver in data:
                    with st.expander(f"{caregiver['name']} (ID: {caregiver['id']})"):
                        st.markdown(f"**Bank Name:** {caregiver['bank_name']}")
                        st.markdown(f"**Bank Account:** {caregiver['bank_account']}")
                        st.markdown(f"**Branch Number:** {caregiver['branch_number']}")
                        
                        # Format salary details
                        salary_data = caregiver.get('salary', {})
                        base_salary = salary_data.get('price', 'N/A')
                        amount = salary_data.get('amount', 'N/A')
                        total = salary_data.get('total', 'N/A')
                        st.markdown(f"**Salary:** Base: {base_salary}, Amount: {amount}, Total: {total}")

                        # Optional: Add Saturday and allowance data
                        saturday_data = caregiver.get('saturday', {})
                        sat_base = saturday_data.get('price', 'N/A')
                        sat_amount = saturday_data.get('amount', 'N/A')
                        sat_total = saturday_data.get('total', 'N/A')
                        st.markdown(f"**Saturday Pay:** Base: {sat_base}, Amount: {sat_amount}, Total: {sat_total}")

                        allowance_data = caregiver.get('allowance', {})
                        allow_base = allowance_data.get('price', 'N/A')
                        allow_amount = allowance_data.get('amount', 'N/A')
                        allow_total = allowance_data.get('total', 'N/A')
                        st.markdown(f"**Allowance:** Base: {allow_base}, Amount: {allow_amount}, Total: {allow_total}")

                        # Total bank balance
                        total_bank = caregiver.get('total_bank', 'N/A')
                        st.markdown(f"**Total Bank Balance:** {total_bank}")

        except RuntimeError as e:
            st.error(str(e))