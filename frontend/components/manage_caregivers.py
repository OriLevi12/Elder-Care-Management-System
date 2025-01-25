import streamlit as st
from api_client import fetch_data, add_data, delete_data, update_salary, generate_pdf

def manage_caregivers():
    st.subheader("Manage Caregivers")
    try:
        caregiver_data = fetch_data("caregivers")
        elderly_data = fetch_data("elderly")
        for caregiver in caregiver_data:
            with st.expander(f"{caregiver['name']} (ID: {caregiver['id']})"):
                # Layout: Delete button on the right
                col1, col2 = st.columns([8, 2])  # Adjust column width ratios
                with col1:
                    st.markdown(f"### {caregiver['name']} (ID: {caregiver['id']})")
                with col2:
                    if st.button(f"❌ Delete", key=f"delete_caregiver_{caregiver['id']}"):
                        delete_data(f"caregivers/{caregiver['id']}")
                        st.success(f"Caregiver {caregiver['name']} deleted successfully!")
                        continue  # Skip rendering tabs for deleted caregiver

                # Tabs for managing caregiver content
                tab1, tab2, tab3, tab4 = st.tabs(["Update Salary", "Generate Payslip", "Assign Elderly", "Cancel assignment"])

                # Update Salary Tab
                with tab1:
                    st.markdown("**Update Salary:**")
                    salary_price = st.number_input("Salary Price", min_value=0.0, step=0.01, key=f"salary_price_{caregiver['id']}")
                    salary_amount = st.number_input("Salary Amount", min_value=0, step=1, key=f"salary_amount_{caregiver['id']}")
                    saturday_price = st.number_input("Saturday Price", min_value=0.0, step=0.01, key=f"saturday_price_{caregiver['id']}")
                    saturday_amount = st.number_input("Saturday Amount", min_value=0, step=1, key=f"saturday_amount_{caregiver['id']}")
                    allowance_price = st.number_input("Allowance Price", min_value=0.0, step=0.01, key=f"allowance_price_{caregiver['id']}")
                    allowance_amount = st.number_input("Allowance Amount", min_value=0, step=1, key=f"allowance_amount_{caregiver['id']}")

                    if st.button(f"Update Salary for {caregiver['name']}", key=f"update_salary_{caregiver['id']}"):
                        payload = {
                            "salary_price": salary_price,
                            "salary_amount": salary_amount,
                            "saturday_price": saturday_price,
                            "saturday_amount": saturday_amount,
                            "allowance_price": allowance_price,
                            "allowance_amount": allowance_amount
                        }
                        update_salary(caregiver['id'], payload)
                        st.success(f"Salary updated for {caregiver['name']}!")

                # Generate Payslip Tab
                with tab2:
                    if st.button(f"Generate Payslip for {caregiver['name']}", key=f"generate_payslip_{caregiver['id']}"):
                        pdf_data = generate_pdf(caregiver['id'])
                        st.download_button(
                            label="Download Payslip",
                            data=pdf_data,
                            file_name=f"caregiver_{caregiver['id']}_payslip.pdf",
                            mime="application/pdf"
                        )

                with tab3:  # New tab for assigning elderly
                    st.markdown("**Assign an Elderly Individual**")
                    elderly_options = {elderly['id']: elderly['name'] for elderly in elderly_data}
                    selected_elderly_id = st.selectbox("Select Elderly", options=list(elderly_options.keys()), format_func=lambda x: elderly_options[x], key=f"select_elderly_{caregiver['id']}")
                    if st.button(f"Assign Elderly to {caregiver['name']}", key=f"assign_elderly_{caregiver['id']}"):
                        payload = {"caregiver_id": caregiver['id'], "elderly_id": selected_elderly_id}
                        add_data("caregiver-assignments", payload)
                        st.success(f"Elderly assigned successfully to {caregiver['name']}!")    

                with tab4:  # New tab for unassign elderly
                    st.markdown("**Unassign an Elderly Individual**")
                    for assignment in caregiver.get("assignments", []):
                        elderly_info = fetch_data(f"elderly/{assignment['elderly_id']}")
                        col1, col2 = st.columns([8, 2])
                        with col1:
                            st.write(f"- {elderly_info['name']} (ID: {elderly_info['id']})")
                        with col2:
                            if st.button(f"Unassign {elderly_info['name']}", key=f"delete_assignment_{assignment['id']}"):
                                delete_data(f"caregiver-assignments/{assignment['id']}")
                                st.success(f"Elderly {elderly_info['name']} removed successfully!")
                            
    except RuntimeError as e:
        st.error(str(e))
