from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import pytesseract
import io

app = FastAPI()


def extract_text(image_file: UploadFile) -> str:
    image = Image.open(image_file.file)
    text = pytesseract.image_to_string(image)
    return text


def generate_invoice_pdf(text1: str, text2: str) -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(100, 750, "Corrected Invoice Generated:")
    pdf.drawString(100, 735, "-----------------------------")

    pdf.drawString(100, 720, "Cropped Invoice Extract:")
    for i, line in enumerate(text1.splitlines()):
        pdf.drawString(100, 700 - i * 15, line)

    offset = 700 - len(text1.splitlines()) * 15 - 20
    pdf.drawString(100, offset, "Full Invoice Extract:")
    for i, line in enumerate(text2.splitlines()):
        pdf.drawString(100,
