import streamlit as st
from api_client import fetch_data, add_data, delete_data, update_salary, generate_pdf

# Title with styling
st.markdown("<h1 style='text-align: center; color: navy;'>Elder Care Management System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar with image and menu
st.sidebar.image("elder_care_logo.png", use_container_width=True)
menu = ["View Data", "Add Data", "Delete Data", "Update Caregiver Salary", "Generate Caregiver PDF"]
choice = st.sidebar.radio("Menu", menu)

if choice == "View Data":
    st.subheader("📊 View Data")
    data_type = st.selectbox("Select data type", ["Elderly", "Caregivers", "Medications"])

    if st.button("Fetch Data"):
        try:
            data = fetch_data(data_type.lower())

            # Handle nested tasks for Elderly
            if data_type == "Elderly":
                for entry in data:
                    if "tasks" in entry:
                        # Include task ID in the description
                        entry["tasks"] = ", ".join([f"{task['id']}: {task['description']} ({task['status']})" for task in entry["tasks"]])
            
            st.dataframe(data)
        except RuntimeError as e:
            st.error(str(e))

elif choice == "Add Data":
    st.subheader("➕ Add Data")
    data_type = st.selectbox("Select data type to add", ["Elderly", "Caregiver", "Task", "Medication"])

    if data_type == "Elderly":
        id = st.number_input("ID", min_value=1, step=1)
        name = st.text_input("Name")
        if st.button("Add Elderly"):
            payload = {"id": id, "name": name}
            try:
                add_data("elderly", payload)
                st.success("Elderly added successfully!")
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
                st.success("Caregiver added successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Task":
        elderly_id = st.number_input("Elderly ID", min_value=1, step=1)
        description = st.text_input("Task Description")
        status = st.text_input("Task Status", value="pending", help="Enter task status (e.g., 'pending', 'completed').")
        if st.button("Add Task"):
            payload = {"description": description, "status": status}
            try:
                add_data(f"elderly/{elderly_id}/tasks", payload)
                st.success("Task added successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Medication":
        name = st.text_input("Medication Name")
        dosage = st.text_input("Dosage")
        frequency = st.text_input("Frequency")
        if st.button("Add Medication"):
            payload = {"name": name, "dosage": dosage, "frequency": frequency}
            try:
                add_data("medications", payload)
                st.success("Medication added successfully!")
            except RuntimeError as e:
                st.error(str(e))

elif choice == "Delete Data":
    st.subheader("🗑️ Delete Data")
    data_type = st.selectbox("Select data type to delete", ["Elderly", "Caregiver", "Task", "Medication"])

    if data_type == "Elderly":
        id = st.number_input(f"{data_type} ID", min_value=1, step=1)
        if st.button("Delete Elderly"):
            endpoint = f"elderly/{id}"
            try:
                delete_data(endpoint)
                st.success(f"Elderly {id} deleted successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Caregiver":
        caregiver_id = st.number_input(f"{data_type} ID", min_value=1, step=1)
        if st.button("Delete Caregiver"):
            endpoint = f"caregivers/{caregiver_id}"
            try:
                delete_data(endpoint)
                st.success(f"Caregiver {caregiver_id} deleted successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Task":
        elderly_id = st.number_input("Elderly ID", min_value=1, step=1)
        task_id = st.number_input(f"Task ID", min_value=1, step=1)
        if st.button("Delete Task"):
            endpoint = f"elderly/{elderly_id}/tasks/{task_id}"
            try:
                delete_data(endpoint)
                st.success(f"Task {task_id} for Elderly {elderly_id} deleted successfully!")
            except RuntimeError as e:
                st.error(str(e))

    elif data_type == "Medication":
        medication_id = st.number_input(f"{data_type} ID", min_value=1, step=1)
        if st.button("Delete Medication"):
            endpoint = f"medications/{medication_id}"
            try:
                delete_data(endpoint)
                st.success(f"Medication {medication_id} deleted successfully!")
            except RuntimeError as e:
                st.error(str(e))

elif choice == "Update Caregiver Salary":
    st.subheader("💰 Update Caregiver Salary")
    caregiver_id = st.number_input("Caregiver ID", min_value=1, step=1)
    salary_price = st.number_input("Salary Price", min_value=0.0, step=0.01)
    salary_amount = st.number_input("Salary Amount", min_value=0, step=1)
    saturday_price = st.number_input("Saturday Price", min_value=0.0, step=0.01)
    saturday_amount = st.number_input("Saturday Amount", min_value=0, step=1)
    allowance_price = st.number_input("Allowance Price", min_value=0.0, step=0.01)
    allowance_amount = st.number_input("Allowance Amount", min_value=0, step=1)

    if st.button("Update Salary"):
        payload = {
            "salary_price": salary_price,
            "salary_amount": salary_amount,
            "saturday_price": saturday_price,
            "saturday_amount": saturday_amount,
            "allowance_price": allowance_price,
            "allowance_amount": allowance_amount
        }
        try:
            update_salary(caregiver_id, payload)
            st.success("Salary updated successfully!")
        except RuntimeError as e:
            st.error(str(e))

elif choice == "Generate Caregiver PDF":
    st.subheader("📄 Generate Caregiver PDF")
    caregiver_id = st.number_input("Caregiver ID", min_value=1, step=1)

    if st.button("Generate PDF"):
        try:
            pdf_data = generate_pdf(caregiver_id)
            st.success(f"PDF for caregiver {caregiver_id} generated successfully!")
            st.download_button(label="Download PDF", data=pdf_data, file_name=f"caregiver_{caregiver_id}_report.pdf", mime="application/pdf")
        except RuntimeError as e:
            st.error(str(e))

