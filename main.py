from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import shutil

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your domain if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-invoice/")
async def generate_invoice(
    cropped: UploadFile = File(...),
    full: UploadFile = File(...)
):
    # Save the uploaded images
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp1:
        shutil.copyfileobj(cropped.file, tmp1)
        cropped_path = tmp1.name

    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp2:
        shutil.copyfileobj(full.file, tmp2)
        full_path = tmp2.name

    # Create a placeholder PDF response
    pdf_path = "corrected_invoice.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, "Corrected Invoice Generated!")
    c.drawString(100, 730, f"Cropped Invoice: {cropped.filename}")
    c.drawString(100, 710, f"Full Invoice: {full.filename}")
    c.save()

    return FileResponse(pdf_path, media_type="application/pdf", filename="corrected_invoice.pdf")
