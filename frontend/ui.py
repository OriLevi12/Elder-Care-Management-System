import streamlit as st
from components.view_data import view_data
from components.add_data import add_data_ui
from components.manage_elderly import manage_elderly
from components.manage_caregivers import manage_caregivers


# Title and sidebar
st.markdown("<h1 style='text-align: center; color: navy;'>Elder Care Management System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.image("media/elder_care_logo.png", use_container_width=True)

# Menu options
menu = ["Elderly & Caregivers", "Manage Elderly", "Manage Caregivers", "Add Elderly/Caregiver"]
choice = st.sidebar.radio("Menu", menu)

# Route actions based on choice
if choice == "Elderly & Caregivers":
    view_data()
elif choice == "Manage Elderly":
    manage_elderly()
elif choice == "Manage Caregivers":
    manage_caregivers()
elif choice == "Add Elderly/Caregiver":
    add_data_ui()

