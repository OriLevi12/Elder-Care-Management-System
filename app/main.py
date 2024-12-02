from fastapi import FastAPI, HTTPException
from fpdf import FPDF
from fastapi.responses import FileResponse
import os

app = FastAPI(
    title="Elder Care Management System",
    description="A system for managing caregivers, medications, tasks, and daily operations for elderly individuals.",
    version="1.0.0"
)

# Directory to save generated PDFs
PDF_DIR = "generated_pdfs"
if not os.path.exists(PDF_DIR):
    os.makedirs(PDF_DIR)

# Initial data
caregivers = []
caregiver_tasks = {}
caregiver_reports = {}

elderly = []
tasks_for_elderly = {}

medications = []
medication_id = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to the Elder Care Management System!"}

# Caregivers Management
@app.post("/caregivers")
def add_caregiver(name: str, id: int, bank_name: str, bank_account: str):
    # Ensure caregiver ID is unique
    if id in caregiver_reports:
        raise HTTPException(status_code=400, detail="Caregiver already exists")
    
    # Add caregiver details
    caregivers.append({"name": name, "id": id, "bank_name": bank_name, "bank_account": bank_account})
    
    # Initialize caregiver report
    caregiver_reports[id] = {
        "name": name,
        "bank_name": bank_name,
        "bank_account": bank_account,
        "salary": {"price": 0, "amount": 0, "total": 0},
        "saturday": {"price": 0, "amount": 0, "total": 0},
        "allowance": {"price": 0, "amount": 0, "total": 0},
        "total_bank": 0
    }
    
    return {"message": f"Caregiver {name} added successfully with bank details"}

@app.get("/caregivers")
def get_caregivers():
    # Retrieve the list of all caregivers
    return {"caregivers": caregivers}

@app.put("/caregivers/{id}/update-all")
def update_all(id: int, salary_price: float = 0, salary_amount: int = 0,
               saturday_price: float = 0, saturday_amount: int = 0,
               allowance_price: float = 0, allowance_amount: int = 0):
    # Update all salary-related fields for a specific caregiver
    if id not in caregiver_reports:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    if salary_price < 0 or salary_amount < 0 or saturday_price < 0 or saturday_amount < 0 or allowance_price < 0 or allowance_amount < 0:
        raise HTTPException(status_code=400, detail="Values must be non-negative")

    caregiver_reports[id]["salary"] = {"price": salary_price, "amount": salary_amount, "total": salary_price * salary_amount}
    caregiver_reports[id]["saturday"] = {"price": saturday_price, "amount": saturday_amount, "total": saturday_price * saturday_amount}
    caregiver_reports[id]["allowance"] = {"price": allowance_price, "amount": allowance_amount, "total": allowance_price * allowance_amount}
    caregiver_reports[id]["total_bank"] = (
        caregiver_reports[id]["salary"]["total"]
        + caregiver_reports[id]["saturday"]["total"]
        + caregiver_reports[id]["allowance"]["total"]
    )
    return {"message": "All values updated successfully", "report": caregiver_reports[id]}

@app.get("/caregivers/{id}/report")
def get_caregiver_report(id: int):
    # Retrieve a detailed report for a specific caregiver
    if id not in caregiver_reports:
        raise HTTPException(status_code=404, detail="Caregiver not found")
    return {"report": caregiver_reports[id]}

@app.get("/caregivers/{id}/generate-pdf")
def generate_pdf(id: int):
    # Ensure caregiver exists
    if id not in caregiver_reports:
        raise HTTPException(status_code=404, detail="Caregiver not found")

    # Retrieve caregiver's report
    report = caregiver_reports[id]

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Pay Slip for {report['name']}", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(80, 10, "Description", 1)
    pdf.cell(30, 10, "Price", 1, align="C")
    pdf.cell(30, 10, "Amount", 1, align="C")
    pdf.cell(30, 10, "Total", 1, align="C")
    pdf.ln()

    # Table Rows
    for key in ["salary", "saturday", "allowance"]:
        pdf.cell(80, 10, key.capitalize(), 1)
        pdf.cell(30, 10, str(report[key]["price"]), 1, align="C")
        pdf.cell(30, 10, str(report[key]["amount"]), 1, align="C")
        pdf.cell(30, 10, str(report[key]["total"]), 1, align="C")
        pdf.ln()

    # Total Bank
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(140, 10, "Total Bank", 1)
    pdf.cell(30, 10, str(report["total_bank"]), 1, align="C")

    # Save PDF
    pdf_path = os.path.join(PDF_DIR, f"caregiver_{id}_report.pdf")
    pdf.output(pdf_path)

    return FileResponse(pdf_path, media_type="application/pdf", filename=f"caregiver_{id}_report.pdf")

# Medications Management
@app.post("/medications")
def add_medication(name: str, dosage: str, frequency: str):
    # Add a new medication
    global medication_id
    medication = {"id": medication_id, "name": name, "dosage": dosage, "frequency": frequency}
    medications.append(medication)
    medication_id += 1
    return {"message": f"Medication {name} added successfully!", "medication": medication}

@app.get("/medications")
def get_medications():
    # Retrieve the list of all medications
    return {"medications": medications}

@app.delete("/medications/{id}")
def delete_medication(id: int):
    # Delete a specific medication by its ID
    global medications
    medications = [med for med in medications if med["id"] != id]
    return {"message": f"Medication with ID {id} deleted successfully!"}
