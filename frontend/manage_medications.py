import streamlit as st
from api_client import fetch_data, delete_data

def manage_medications():
    st.subheader("💊 Manage Medications")
    try:
        medication_data = fetch_data("medications")
        for medication in medication_data:
            st.markdown(f"### {medication['name']} (ID: {medication['id']})")
            st.write(f"Dosage: {medication['dosage']}")
            st.write(f"Frequency: {medication['frequency']}")

            if st.button(f"Delete {medication['name']}", key=f"delete_medication_{medication['id']}"):
                delete_data(f"medications/{medication['id']}")
                st.success(f"Medication {medication['name']} deleted successfully!")
    except RuntimeError as e:
        st.error(str(e))

