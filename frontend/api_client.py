import requests
import streamlit as st

BASE_URL = "http://backend:8000"

# Authentication functions
def register_user(email: str, password: str, full_name: str):
    """
    Register a new user.
    """
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "full_name": full_name
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error registering user: {e}")

def login_user(email: str, password: str):
    """
    Login a user and return access token.
    """
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error logging in: {e}")

def get_auth_headers():
    """
    Get authentication headers for API requests.
    """
    token = st.session_state.get("access_token")
    if not token:
        raise RuntimeError("No access token found. Please login first.")
    return {"Authorization": f"Bearer {token}"}

def fetch_data(endpoint):
    """
    Fetch data from the API for the given endpoint with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from {endpoint}: {e}")

def add_data(endpoint, payload):
    """
    Add data to the API for the given endpoint with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error adding data to {endpoint}: {e}")

def delete_data(endpoint):
    """
    Delete data from the API for the given endpoint with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.delete(f"{BASE_URL}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error deleting data from {endpoint}: {e}")

def update_salary(caregiver_id, payload):
    """
    Update the salary of a caregiver with the given ID with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.put(f"{BASE_URL}/caregivers/{caregiver_id}/update-salary", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error updating salary for caregiver {caregiver_id}: {e}")

def update_task_status(elderly_id, task_id, new_status):
    """
    Update the status of a task for a specific elderly person with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.put(
            f"{BASE_URL}/elderly/{elderly_id}/tasks/{task_id}/status",
            params={"new_status": new_status},
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error updating task status for Task {task_id}: {e}")

def generate_pdf(caregiver_id):
    """
    Generate a PDF report for a caregiver with the given ID with authentication.
    """
    try:
        headers = get_auth_headers()
        response = requests.get(f"{BASE_URL}/caregivers/{caregiver_id}/generate-pdf", headers=headers)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error generating PDF for caregiver {caregiver_id}: {e}")
