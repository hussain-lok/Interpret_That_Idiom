from fpdf import FPDF
from pathlib import Path
import json
# Create PDF class
class IdiomPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Interpret That Idiom! - Idiom Cards", ln=True, align="C")
        self.ln(5)

    def add_idiom_card(self, idiom_text):
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, f"Idiom: {idiom_text}", border=1)
        self.ln(2)

def create_idioms(json_file_path, output_file_path):
    json_path = Path(json_file_path)
    with open(json_path, "r") as f:
        data = json.load(f)

    idioms = data["Idioms"]
    num_blanks = data["Blanks"]

    # Add blank idioms
    idioms += [""] * num_blanks

    # Create PDF
    pdf = IdiomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add idiom cards
    for idiom in idioms:
        pdf.add_idiom_card(idiom)

    # Save PDF
    pdf.output(output_file_path)
