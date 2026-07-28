from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = APIRouter(prefix="/generator", tags=["Artifact Compiler"])

class AssetPayload(BaseModel):
    brand_name: str
    primary_color: str
    tagline: str

TMP_DIR = "/tmp/studio_outputs" if os.name != 'nt' else "C:\\temp\\studio_outputs"
TEMPLATE_PATH = "backend/app/templates/landing.html"
os.makedirs(TMP_DIR, exist_ok=True)

@router.post("/build-package")
async def build_brand_package(payload: AssetPayload):
    pdf_filename = os.path.join(TMP_DIR, f"{payload.brand_name}_BrandBook.pdf")
    zip_filename = os.path.join(TMP_DIR, f"{payload.brand_name}_CompleteKit.zip")
    
    try:
        # 1. Compile Brand Guidelines Document (PDF)
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"BRAND GUIDELINES: {payload.brand_name.upper()}")
        c.drawString(100, 720, f"Tagline: {payload.tagline}")
        c.drawString(100, 690, f"Primary Creative Brand Color: {payload.primary_color}")
        c.save()
        
        # 2. Render Template HTML File
        if os.path.exists(TEMPLATE_PATH):
            with open(TEMPLATE_PATH, "r") as f:
                html_content = f.read()
            html_content = html_content.replace("{{ brand_name }}", payload.brand_name)
            html_content = html_content.replace("{{ tagline }}", payload.tagline)
            html_content = html_content.replace("{{ primary_color }}", payload.primary_color)
        else:
            html_content = f"<html><body style='background:{payload.primary_color};'><h1>{payload.brand_name}</h1><p>{payload.tagline}</p></body></html>"

        html_out_path = os.path.join(TMP_DIR, "index.html")
        with open(html_out_path, "w") as f:
            f.write(html_content)
        
        # 3. Compile Compressed Asset Kit (ZIP)
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(pdf_filename, arcname=f"BrandBook.pdf")
            zipf.write(html_out_path, arcname="landing_page/index.html")
            
        return FileResponse(path=zip_filename, filename=f"{payload.brand_name}_Kit.zip", media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
