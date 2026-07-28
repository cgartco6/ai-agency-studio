from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

router = APIRouter(prefix="/generator", tags=["Artifact Compiler"])

TMP_DIR = "/tmp/studio_outputs" if os.name != 'nt' else "C:\\temp\\studio_outputs"
TEMPLATE_BASE_PATH = "backend/app/templates"
os.makedirs(TMP_DIR, exist_ok=True)

@router.post("/build-package")
async def build_brand_package(
    brand_name: str = Form(...),
    primary_color: str = Form(...),
    tagline: str = Form(...),
    template_selection: str = Form("landing.html") # Accepts landing.html, creative.html, or corporate.html
):
    pdf_filename = os.path.join(TMP_DIR, f"{brand_name}_BrandBook.pdf")
    zip_filename = os.path.join(TMP_DIR, f"{brand_name}_CompleteKit.zip")
    
    try:
        # 1. Generate PDF Identity Guide
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"BRAND BLUEPRINT: {brand_name.upper()}")
        c.drawString(100, 720, f"Core Stance: {tagline}")
        c.drawString(100, 690, f"Primary Hex Asset: {primary_color}")
        c.save()
        
        # 2. Extract and Inject User Selections into the Selected Layout File
        selected_file_path = os.path.join(TEMPLATE_BASE_PATH, template_selection)
        if os.path.exists(selected_file_path):
            with open(selected_file_path, "r") as f:
                html_content = f.read()
            html_content = html_content.replace("{{ brand_name }}", brand_name)
            html_content = html_content.replace("{{ tagline }}", tagline)
            html_content = html_content.replace("{{ primary_color }}", primary_color)
        else:
            html_content = f"<html><body><h1>{brand_name}</h1><p>{tagline}</p></body></html>"

        html_out_path = os.path.join(TMP_DIR, "index.html")
        with open(html_out_path, "w") as f:
            f.write(html_content)
        
        # 3. Compile Production Output ZIP Bundle
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(pdf_filename, arcname="BrandBook.pdf")
            zipf.write(html_out_path, arcname="index.html")
            
        return FileResponse(path=zip_filename, filename=f"{brand_name}_Kit.zip", media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
