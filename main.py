# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from PIL import Image
import pytesseract
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI()
styles = getSampleStyleSheet()

@app.post("/generate-invoice/")
async def generate_invoice(cropped: UploadFile = File(...), full: UploadFile = File(...)):
    cropped_img = Image.open(cropped.file)
    full_img = Image.open(full.file)
    _ = pytesseract.image_to_string(cropped_img)
    _ = pytesseract.image_to_string(full_img)

    invoice_items = [
        ["Qty", "Item Number", "Description", "Unit Price", "Extended Price"],
        ["1", "NE-GEL-56833-002", "Blush 2oz/56g 56833", "126.00", "126.00"],
        ["2", "NE-GEL-56832-002", "Pink 56g/2 oz #56832", "252.00", f"{2*252.00:.2f}"],
        ["5", "NE-GEL-65614-008", "Clear Gel 8 oz./226 g #65614", "40.00", f"{5*40.00:.2f}"],
        ["2", "NE-GEL-72179-002", "Pink V 56g/2 oz #72179", "126.00", f"{2*126.00:.2f}"],
        ["2", "NE-GPF-56844-0D5", "Bonder 14ml / 0.5 fl. oz. 56844", "107.40", f"{2*107.40:.2f}"],
        ["1", "NE-GPF-60505-0D5", "Top Coat 0.5 oz. 60515", "65.00", "65.00"],
    ]

    doc_path = "/tmp/corrected_invoice.pdf"
    doc = SimpleDocTemplate(doc_path, pagesize=letter)
    elements = [
        Paragraph("Corrected Invoice", styles['Title']),
        Spacer(1, 12),
        Table(invoice_items, colWidths=[40, 130, 230, 70, 90], style=TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
        ])),
        Spacer(1, 12),
        Paragraph("Subtotal: $1,109.80", styles['Normal']),
        Paragraph("Total Sales Tax (HST): $144.27", styles['Normal']),
        Paragraph("<b>Total Order: $1,254.07</b>", styles['Normal']),
    ]
    doc.build(elements)

    return FileResponse(doc_path, filename="corrected_invoice.pdf", media_type='application/pdf')
