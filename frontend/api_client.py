import requests

BASE_URL = "http://backend:8000"

def fetch_data(endpoint):
    """
    Fetch data from the API for the given endpoint.
    """
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching data from {endpoint}: {e}")

def add_data(endpoint, payload):
    """
    Add data to the API for the given endpoint.
    """
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error adding data to {endpoint}: {e}")

def delete_data(endpoint):
    """
    Delete data from the API for the given endpoint.
    """
    try:
        response = requests.delete(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error deleting data from {endpoint}: {e}")

def update_salary(caregiver_id, payload):
    """
    Update the salary of a caregiver with the given ID.
    """
    try:
        response = requests.put(f"{BASE_URL}/caregivers/{caregiver_id}/update-salary", json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error updating salary for caregiver {caregiver_id}: {e}")

def update_task_status(elderly_id, task_id, new_status):
    """
    Update the status of a task for a specific elderly person.
    """
    try:
        response = requests.put(
            f"{BASE_URL}/elderly/{elderly_id}/tasks/{task_id}/status",
            params={"new_status": new_status}  # Pass the new status as a parameter
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error updating task status for Task {task_id}: {e}")

def generate_pdf(caregiver_id):
    """
    Generate a PDF report for a caregiver with the given ID.
    """
    try:
        response = requests.get(f"{BASE_URL}/caregivers/{caregiver_id}/generate-pdf")
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error generating PDF for caregiver {caregiver_id}: {e}")
