from fpdf import FPDF
from datetime import datetime

class PDFGenerator:
    def __init__(self, caregiver_name: str):
        self.pdf = FPDF()
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", size=12)
        self.caregiver_name = caregiver_name
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def add_title(self):
        # Set fill color for the title rectangle (light gray)
        self.pdf.set_fill_color(220, 220, 220)
        self.pdf.set_text_color(0, 51, 102)  # Dark blue text color
        self.pdf.set_font("Helvetica", style="B", size=16)
        
        # Title text with caregiver's name and current date
        title = f"  {self.caregiver_name}   -   {self.current_date}  "
        
        # Create a rectangle for the title matching the table width (180 units)
        self.pdf.cell(180, 15, title, border=1, align='C', fill=True)
        self.pdf.ln(20)  # Space after the title

    def add_table(self, caregiver):
        # Set table header background color (blue) and text color (white)
        self.pdf.set_fill_color(0, 102, 204)  # Blue background
        self.pdf.set_text_color(255, 255, 255)  # White text color
        self.pdf.set_font("Helvetica", style="B", size=12)

        # Table header
        headers = ["Description", "Price", "Amount", "Total"]
        col_widths = [60, 40, 40, 40]

        for header, width in zip(headers, col_widths):
            self.pdf.cell(width, 10, header, border=1, align='C', fill=True)
        self.pdf.ln()

        # Reset text color to black for table rows
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_font("Helvetica", size=12)

        # Table rows
        rows = [
            ("Salary", caregiver.salary["price"], caregiver.salary["amount"], caregiver.salary["total"]),
            ("Saturday Pay", caregiver.saturday["price"], caregiver.saturday["amount"], caregiver.saturday["total"]),
            ("Allowance", caregiver.allowance["price"], caregiver.allowance["amount"], caregiver.allowance["total"]),
        ]

        # Alternate row background colors (white and light blue)
        fill_colors = [(255, 255, 255), (230, 247, 255)]  # White and Light Blue
        for i, (desc, price, amount, total) in enumerate(rows):
            fill_color = fill_colors[i % 2]
            self.pdf.set_fill_color(*fill_color)
            fill = True

            self.pdf.cell(col_widths[0], 10, desc, border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[1], 10, f"{price:.2f}", border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[2], 10, str(amount), border=1, align='C', fill=fill)
            self.pdf.cell(col_widths[3], 10, f"{total:.2f}", border=1, align='C', fill=fill)
            self.pdf.ln()

        # Total Bank row with background color (light yellow)
        self.pdf.set_font("Helvetica", style="B", size=12)
        self.pdf.set_fill_color(255, 255, 204)  # Light yellow
        self.pdf.set_text_color(0, 0, 0)  # Ensure text color is black
        self.pdf.cell(col_widths[0] + col_widths[1] + col_widths[2], 10, "Total Bank", border=1, align='C', fill=True)
        self.pdf.cell(col_widths[3], 10, f"{caregiver.total_bank:.2f}", border=1, align='C', fill=True)
        self.pdf.ln(20)

    def add_footer(self, caregiver):
        # Reset text color to black
        self.pdf.set_text_color(0, 0, 0)

        # Add current date
        self.pdf.set_font("Helvetica", size=12)
        self.pdf.cell(0, 10, f"Report Date: {self.current_date}", ln=True, align='L')
        self.pdf.ln(10)

        # Add bank transfer details in dark green
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
    from models.caregiver import Caregiver  # Lazy Import to avoid circular import
    pdf_gen = PDFGenerator(caregiver_name=caregiver.name)
    pdf_gen.add_title()
    pdf_gen.add_table(caregiver)
    pdf_gen.add_footer(caregiver)

    filename = f"caregiver_{caregiver.id}_report.pdf"
    return pdf_gen.save_pdf(filename)
