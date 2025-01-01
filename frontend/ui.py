import streamlit as st
from api_client import fetch_data, add_data, delete_data, update_salary, generate_pdf, update_task_status

# Title with styling
st.markdown("<h1 style='text-align: center; color: navy;'>Elder Care Management System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar with image and menu
st.sidebar.image("elder_care_logo.png", use_container_width = True)
menu = ["View Data", "Manage Elderly", "Manage Caregivers", "Manage Medications", "Add Data"]
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

            # Handle salary for Caregivers
            if data_type == "Caregivers":
                for entry in data:
                    salary_data = entry.get('salary', {})
                    entry["salary"] = f"Base: {salary_data.get('price', 'N/A')}, Amount: {salary_data.get('amount', 'N/A')}, Total: {                                        salary_data.get('total', 'N/A')}"

            st.dataframe(data)
        except RuntimeError as e:
            st.error(str(e))

elif choice == "Manage Elderly":
    st.subheader("👴 Manage Elderly")

    # Fetch Elderly Data
    try:
        elderly_data = fetch_data("elderly")
        for elderly in elderly_data:
            st.markdown(f"### {elderly['name']} (ID: {elderly['id']})")

            # Display Tasks
            if "tasks" in elderly:
                st.markdown("**Tasks:**")
                for task in elderly["tasks"]:
                    st.write(f"- {task['id']}: {task['description']} ({task['status']})")

                    # Update Task Status
                    new_status = st.text_input(f"Update Status for Task {task['id']}", value=task['status'], key=f"update_status_{task['id']}")
                    if st.button(f"Update Task {task['id']} Status", key=f"update_task_status_{task['id']}"):
                        update_task_status(elderly['id'], task['id'], new_status)
                        st.success(f"Task {task['id']} status updated to {new_status}!")

                    # Delete Task
                    if st.button(f"Delete Task {task['id']}", key=f"delete_task_{task['id']}"):
                        delete_data(f"elderly/{elderly['id']}/tasks/{task['id']}")
                        st.success(f"Task {task['id']} deleted successfully!")

            # Add Task
            st.markdown("**Add Task:**")
            description = st.text_input(f"Task Description for {elderly['name']}", key=f"task_description_{elderly['id']}")
            status = st.text_input("Task Status", value="pending", key=f"task_status_{elderly['id']}")
            if st.button(f"Add Task to {elderly['name']}", key=f"add_task_{elderly['id']}"):
                payload = {"description": description, "status": status}
                add_data(f"elderly/{elderly['id']}/tasks", payload)
                st.success(f"Task added successfully to {elderly['name']}!")

            # Delete Elderly
            if st.button(f"Delete {elderly['name']}", key=f"delete_elderly_{elderly['id']}"):
                delete_data(f"elderly/{elderly['id']}")
                st.success(f"Elderly {elderly['name']} deleted successfully!")

    except RuntimeError as e:
        st.error(str(e))

elif choice == "Manage Caregivers":
    st.subheader("🧑‍⚕️ Manage Caregivers")

    # Fetch Caregiver Data
    try:
        caregiver_data = fetch_data("caregivers")
        for caregiver in caregiver_data:
            st.markdown(f"### {caregiver['name']} (ID: {caregiver['id']})")

            # Update Salary
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

            # Generate PDF
            if st.button(f"Generate PDF for {caregiver['name']}", key=f"generate_pdf_{caregiver['id']}"):
                pdf_data = generate_pdf(caregiver['id'])
                st.download_button(label="Download PDF", data=pdf_data, file_name=f"caregiver_{caregiver['id']}_report.pdf", mime="application/pdf")

            # Delete Caregiver
            if st.button(f"Delete {caregiver['name']}", key=f"delete_caregiver_{caregiver['id']}"):
                delete_data(f"caregivers/{caregiver['id']}")
                st.success(f"Caregiver {caregiver['name']} deleted successfully!")

    except RuntimeError as e:
        st.error(str(e))

elif choice == "Manage Medications":
    st.subheader("💊 Manage Medications")

    # Fetch Medication Data
    try:
        medication_data = fetch_data("medications")
        for medication in medication_data:
            st.markdown(f"### {medication['name']} (ID: {medication['id']})")
            st.write(f"Dosage: {medication['dosage']}")
            st.write(f"Frequency: {medication['frequency']}")

            # Delete Medication
            if st.button(f"Delete {medication['name']}", key=f"delete_medication_{medication['id']}"):
                delete_data(f"medications/{medication['id']}")
                st.success(f"Medication {medication['name']} deleted successfully!")

    except RuntimeError as e:
        st.error(str(e))

elif choice == "Add Data":
    st.subheader("➕ Add Data")
    data_type = st.selectbox("Select data type to add", ["Elderly", "Caregiver", "Medication"])

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

