import streamlit as st
from api_client import fetch_data, add_data, delete_data, update_task_status

def manage_elderly():
    st.subheader("👴 Manage Elderly")
    try:
        elderly_data = fetch_data("elderly")
        for elderly in elderly_data:
            st.markdown(f"### {elderly['name']} (ID: {elderly['id']})")

            if "tasks" in elderly:
                st.markdown("**Tasks:**")
                for task in elderly["tasks"]:
                    st.write(f"- {task['id']}: {task['description']} ({task['status']})")

                    new_status = st.text_input(f"Update Status for Task {task['id']}", value=task['status'], key=f"update_status_{task['id']}")
                    if st.button(f"Update Task {task['id']} Status", key=f"update_task_status_{task['id']}"):
                        update_task_status(elderly['id'], task['id'], new_status)
                        st.success(f"Task {task['id']} status updated to {new_status}!")

                    if st.button(f"Delete Task {task['id']}", key=f"delete_task_{task['id']}"):
                        delete_data(f"elderly/{elderly['id']}/tasks/{task['id']}")
                        st.success(f"Task {task['id']} deleted successfully!")

            description = st.text_input(f"Task Description for {elderly['name']}", key=f"task_description_{elderly['id']}")
            status = st.text_input("Task Status", value="pending", key=f"task_status_{elderly['id']}")
            if st.button(f"Add Task to {elderly['name']}", key=f"add_task_{elderly['id']}"):
                payload = {"description": description, "status": status}
                add_data(f"elderly/{elderly['id']}/tasks", payload)
                st.success(f"Task added successfully to {elderly['name']}!")

            if st.button(f"Delete {elderly['name']}", key=f"delete_elderly_{elderly['id']}"):
                delete_data(f"elderly/{elderly['id']}")
                st.success(f"Elderly {elderly['name']} deleted successfully!")
    except RuntimeError as e:
        st.error(str(e))

