from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self, title: str):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=12)
        self.title = title

    def add_title(self, caregiver_name: str, caregiver_id: int):
        self.pdf.set_font("Helvetica", style="B", size=16)
        self.pdf.cell(0, 10, txt=self.title, ln=True, align='C')
        self.pdf.ln(10)

    def add_table(self, caregiver):
        self.pdf.set_font("Helvetica", style="B", size=12)

        # Table header
        headers = ["Description", "Price", "Amount", "Total"]
        col_widths = [60, 40, 40, 40]

        for header, width in zip(headers, col_widths):
            self.pdf.cell(width, 10, header, border=1, align='C')
        self.pdf.ln()

        # Table rows
        rows = [
            ("Salary", caregiver.salary["price"], caregiver.salary["amount"], caregiver.salary["total"]),
            ("Saturday Pay", caregiver.saturday["price"], caregiver.saturday["amount"], caregiver.saturday["total"]),
            ("Allowance", caregiver.allowance["price"], caregiver.allowance["amount"], caregiver.allowance["total"]),
        ]

        self.pdf.set_font("Helvetica", size=12)
        for desc, price, amount, total in rows:
            self.pdf.cell(col_widths[0], 10, desc, border=1, align='C')
            self.pdf.cell(col_widths[1], 10, f"{price:.2f}", border=1, align='C')
            self.pdf.cell(col_widths[2], 10, str(amount), border=1, align='C')
            self.pdf.cell(col_widths[3], 10, f"{total:.2f}", border=1, align='C')
            self.pdf.ln()

        # Total Bank row
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.cell(col_widths[0] + col_widths[1] + col_widths[2], 10, "Total Bank", border=1, align='C')
        self.pdf.cell(col_widths[3], 10, f"{caregiver.total_bank:.2f}", border=1, align='C')
        self.pdf.ln(20)

    def add_footer(self, caregiver):
        # Add current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.pdf.set_font("Helvetica", size=12)
        self.pdf.cell(0, 10, f"Report Date: {current_date}", ln=True, align='L')
        self.pdf.ln(10)

        # Add bank transfer details
        transfer_details = (
            f"Transfer to: Bank {caregiver.bank_name}, "
            f"Account {caregiver.bank_account}, "
            f"Branch {caregiver.branch_number}"
        )
        self.pdf.cell(0, 10, transfer_details, ln=True, align='L')

    def save_pdf(self, filename: str):
        try:
            self.pdf.output(filename)
        except Exception as e:
            print(f"Error creating PDF: {e}")
        return filename

def generate_caregiver_pdf(caregiver):
    from models.caregiver import Caregiver  # Lazy Import to avoid circular import
    pdf_gen = PDFGenerator(title=f"Caregiver Report for {caregiver.name}")
    pdf_gen.add_title(caregiver.name, caregiver.id)
    pdf_gen.add_table(caregiver)
    pdf_gen.add_footer(caregiver)

    filename = f"caregiver_{caregiver.id}_report.pdf"
    return pdf_gen.save_pdf(filename)
