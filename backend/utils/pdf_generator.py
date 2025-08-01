from fpdf import FPDF
from datetime import datetime


class PDFGenerator:
    def __init__(self, caregiver_name: str):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=12)
        self.caregiver_name = caregiver_name
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def add_title(self, caregiver):
        self.pdf.set_fill_color(220, 220, 220)
        self.pdf.set_text_color(0, 51, 102)
        self.pdf.set_font("Helvetica", style="B", size=16)

        title = f"  {self.caregiver_name} (ID: {caregiver.custom_id})   -   {self.current_date}  "
        self.pdf.cell(180, 15, title, border=1, align='C', fill=True)
        self.pdf.ln(20)

    def add_table(self, caregiver):
        self.pdf.set_fill_color(0, 102, 204)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.set_font("Helvetica", style="B", size=12)

        headers = ["Description", "Price", "Amount", "Total"]
        col_widths = [60, 40, 40, 40]

        for header, width in zip(headers, col_widths):
            self.pdf.cell(width, 10, header, border=1, align='C', fill=True)
        self.pdf.ln()

        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Helvetica", size=12)

        rows = [
            ("Salary", caregiver.salary["price"], caregiver.salary["amount"], caregiver.salary["total"]),
            ("Saturday Pay", caregiver.saturday["price"], caregiver.saturday["amount"], caregiver.saturday["total"]),
            ("Allowance", caregiver.allowance["price"], caregiver.allowance["amount"], caregiver.allowance["total"]),
        ]

        fill_colors = [(255, 255, 255), (230, 247, 255)]
        for i, (desc, price, amount, total) in enumerate(rows):
            fill_color = fill_colors[i % 2]
            self.pdf.set_fill_color(*fill_color)
            fill = True

            self.pdf.cell(col_widths[0], 10, desc, border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[1], 10, f"{price:.2f}", border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[2], 10, str(amount), border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[3], 10, f"{total:.2f}", border=1, align='C', fill=fill)
            self.pdf.ln()

        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.set_fill_color(255, 255, 204)
        self.pdf.cell(col_widths[0] + col_widths[1] + col_widths[2], 10, "Total Bank", border=1, align='C', fill=True)
        self.pdf.cell(col_widths[3], 10, f"{caregiver.total_bank:.2f}", border=1, align='C', fill=True)
        self.pdf.ln(20)

    def add_footer(self, caregiver):
        self.pdf.set_text_color(0, 0, 0)

        self.pdf.set_font("Helvetica", size=12)
        self.pdf.cell(0, 10, f"Report Date: {self.current_date}", ln=True, align='L')
        self.pdf.ln(10)

        self.pdf.set_text_color(0, 100, 0)
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
    pdf_gen = PDFGenerator(caregiver_name=caregiver.name)
    pdf_gen.add_title(caregiver)  # Pass caregiver object to access custom_id
    pdf_gen.add_table(caregiver)
    pdf_gen.add_footer(caregiver)

    # Use custom_id for filename (user-friendly ID)
    filename = f"caregiver_{caregiver.custom_id}_report.pdf"
    return pdf_gen.save_pdf(filename)
