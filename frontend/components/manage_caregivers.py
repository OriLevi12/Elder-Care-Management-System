import streamlit as st
from api_client import fetch_data, delete_data, update_salary, generate_pdf

def manage_caregivers():
    st.subheader("🧑‍⚕️ Manage Caregivers")
    try:
        caregiver_data = fetch_data("caregivers")
        for caregiver in caregiver_data:
            st.markdown(f"### {caregiver['name']} (ID: {caregiver['id']})")

            # Update Salary Section
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

            # Generate PDF Section
            if st.button(f"Generate PDF for {caregiver['name']}", key=f"generate_pdf_{caregiver['id']}"):
                pdf_data = generate_pdf(caregiver['id'])
                st.download_button(label="Download PDF", data=pdf_data, file_name=f"caregiver_{caregiver['id']}_report.pdf", mime="application/pdf")

            # Delete Caregiver Section
            if st.button(f"Delete {caregiver['name']}", key=f"delete_caregiver_{caregiver['id']}"):
                delete_data(f"caregivers/{caregiver['id']}")
                st.success(f"Caregiver {caregiver['name']} deleted successfully!")
    except RuntimeError as e:
        st.error(str(e))

