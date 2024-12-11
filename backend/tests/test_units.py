import pytest
from models.caregiver import Caregiver
from models.elderly import Elderly
from models.task import Task

def test_add_caregiver():
    caregiver = Caregiver(name="John Doe", id=1, bank_name="Bank A", bank_account="12345", branch_number="001")
    assert caregiver.name == "John Doe"
    assert caregiver.bank_name == "Bank A"

def test_update_salary():
    caregiver = Caregiver(name="Jane Doe", id=2, bank_name="Bank B", bank_account="67890", branch_number="002")
    caregiver.update_salary(1000, 2, 200, 3, 150, 4)
    assert caregiver.total_bank == (1000 * 2) + (200 * 3) + (150 * 4)

def test_add_elderly():
    elderly = Elderly(id=1, name="Alice")
    assert elderly.name == "Alice"

def test_add_task():
    elderly = Elderly(id=1, name="Alice")
    elderly.add_task(Task(description="Take medicine"))
    assert len(elderly.tasks) == 1
    assert elderly.tasks[0].description == "Take medicine"

def test_update_task_status():
    task = Task(description="Go for a walk")
    task.update_status("completed")
    assert task.status == "completed"
