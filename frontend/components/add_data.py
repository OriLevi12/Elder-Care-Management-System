import streamlit as st
from api_client import add_data, fetch_data

def add_data_ui():
    st.subheader("➕ Add Elderly & Caregivers")


    st.markdown(
        """
        <style>
        div[data-testid="stExpander"] {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 6px;
            background-color: #f9f9f9;
            transition: all 0.3s ease-in-out;
        }

        div[data-testid="stExpander"]:hover {
            background-color: #e9f5ff;
            border: 1px solid #4fdee3;
        }

        .expander-title {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            display: flex;
            align-items: center;
        }

        .icon {
            margin-right: 8px;
            font-size: 18px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    
    data_type = st.radio("Select Profile Type", ["👴 Elderly", "👨‍⚕️ Caregiver"])

   
    if data_type == "👴 Elderly":
        with st.expander("➕ Add Elderly", expanded=True):
            st.markdown("#### 👴 Enter Elderly Details")
            id = st.number_input("🔢 ID", min_value=1, step=1)
            name = st.text_input("📝 Name")
            if st.button("➕ Add Elderly", use_container_width=True):
                payload = {"id": id, "name": name}
                try:
                    add_data("elderly", payload)
                    st.success(f"👴 Elderly {name} added successfully!")
                except RuntimeError as e:
                    st.error(str(e))

    
    elif data_type == "👨‍⚕️ Caregiver":
        with st.expander("➕ Add Caregiver", expanded=True):
            st.markdown("#### 👨‍⚕️ Enter Caregiver Details")
            id = st.number_input("🔢 ID", min_value=1, step=1)
            name = st.text_input("📝 Name")
            bank_name = st.text_input("🏦 Bank Name")
            bank_account = st.text_input("🏦 Bank Account")
            branch_number = st.text_input("🏦 Branch Number")

            if st.button("➕ Add Caregiver", use_container_width=True):
                payload = {
                    "id": id,
                    "name": name,
                    "bank_name": bank_name,
                    "bank_account": bank_account,
                    "branch_number": branch_number
                }
                try:
                    add_data("caregivers", payload)
                    st.success(f"👨‍⚕️ Caregiver {name} added successfully!")
                except RuntimeError as e:
                    st.error(str(e))
 