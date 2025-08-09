import pytest
from models.caregiver import Caregiver
from models.elderly import Elderly
from models.task import Task

# Test for the Caregiver model
def test_create_caregiver():
    caregiver = Caregiver(
        custom_id=1,
        name="John Doe",
        bank_name="Bank A",
        bank_account="12345678",
        branch_number="001",
        user_id=1
    )
    assert caregiver.name == "John Doe"
    assert caregiver.bank_name == "Bank A"
    assert caregiver.bank_account == "12345678"
    assert caregiver.branch_number == "001"
    assert caregiver.custom_id == 1
    assert caregiver.user_id == 1

def test_update_caregiver_salary():
    caregiver = Caregiver(
        custom_id=1,
        name="John Doe",
        bank_name="Bank A",
        bank_account="12345678",
        branch_number="001",
        user_id=1,
        salary={"price": 0, "amount": 0, "total": 0},
        saturday={"price": 0, "amount": 0, "total": 0},
        allowance={"price": 0, "amount": 0, "total": 0},
    )
    # Update the salary
    caregiver.salary = {"price": 100, "amount": 2, "total": 200}
    caregiver.saturday = {"price": 50, "amount": 4, "total": 200}
    caregiver.allowance = {"price": 30, "amount": 3, "total": 90}
    caregiver.total_bank = caregiver.salary["total"] + caregiver.saturday["total"] + caregiver.allowance["total"]

    assert caregiver.salary["total"] == 200
    assert caregiver.saturday["total"] == 200
    assert caregiver.allowance["total"] == 90
    assert caregiver.total_bank == 490

# Test for the Elderly model
def test_create_elderly():
    elderly = Elderly(custom_id=1, name="Alice", user_id=1)
    assert elderly.custom_id == 1
    assert elderly.name == "Alice"
    assert elderly.user_id == 1

def test_add_task_to_elderly():
    elderly = Elderly(custom_id=1, name="Alice", user_id=1)
    task = Task(id=1, description="Take medicine", status="pending")
    elderly.tasks.append(task)

    assert len(elderly.tasks) == 1
    assert elderly.tasks[0].description == "Take medicine"
    assert elderly.tasks[0].status == "pending"

# Test for the Task model
def test_create_task():
    task = Task(id=1, description="Visit doctor", status="pending")
    assert task.description == "Visit doctor"
    assert task.status == "pending"

def test_update_task_status():
    task = Task(id=1, description="Visit doctor", status="pending")
    task.status = "completed"

    assert task.status == "completed"
