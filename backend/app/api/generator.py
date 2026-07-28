from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import UserWorkspace
import os
import zipfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

router = APIRouter(prefix="/generator", tags=["Artifact Compiler"])

TMP_DIR = "/tmp/studio_outputs" if os.name != 'nt' else "C:\\temp\\studio_outputs"
TEMPLATE_BASE_PATH = "backend/app/templates"

@router.post("/build-package")
async def build_brand_package(
    workspace_id: int = Form(...),
    brand_name: str = Form(...),
    primary_color: str = Form(...),
    tagline: str = Form(...),
    template_selection: str = Form("landing.html"),
    db: Session = Depends(get_db)
):
    pdf_filename = os.path.join(TMP_DIR, f"{brand_name}_BrandBook.pdf")
    zip_filename = os.path.join(TMP_DIR, f"{brand_name}_CompleteKit.zip")
    
    # Verify the current multi-user payment profile status
    user_ws = db.query(UserWorkspace).filter(UserWorkspace.id == workspace_id).first()
    is_unverified_trial = True
    
    if user_ws and user_ws.currency == "ZAR_VERIFIED":
        is_unverified_trial = False
    
    try:
        # 1. Compile Brand Blueprint PDF Layout
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.drawString(100, 750, f"BRAND BLUEPRINT: {brand_name.upper()}")
        c.drawString(100, 720, f"Core Stance: {tagline}")
        c.drawString(100, 690, f"Primary Hex Asset: {primary_color}")
        
        # 2. Inject Watermark Overlay Only If Account Settlement Clearing Is Pending
        if is_unverified_trial:
            c.saveState()
            c.setFont("Helvetica-Bold", 42)
            c.setFillColor(colors.HexColor("#ef4444"), alpha=0.12)
            c.translate(300, 400)
            c.rotate(45)
            c.drawCentredString(0, 0, "UNVERIFIED TRIAL WORKSPACE")
            c.restoreState()
            
        c.save()
        
        # 3. Handle Landing Page Template Extractions
        selected_file_path = os.path.join(TEMPLATE_BASE_PATH, template_selection)
        if os.path.exists(selected_file_path):
            with open(selected_file_path, "r") as f:
                html_content = f.read()
            html_content = html_content.replace("{{ brand_name }}", brand_name)
            html_content = html_content.replace("{{ tagline }}", tagline)
            html_content = html_content.replace("{{ primary_color }}", primary_color)
        else:
            html_content = f"<html><body><h1>{brand_name}</h1></body></html>"

        html_out_path = os.path.join(TMP_DIR, "index.html")
        with open(html_out_path, "w") as f:
            f.write(html_content)
        
        # 4. Pack final output compilation ZIP 
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            zipf.write(pdf_filename, arcname="Unverified_Trial_BrandBook.pdf" if is_unverified_trial else "BrandBook.pdf")
            zipf.write(html_out_path, arcname="index.html")
            
        return FileResponse(path=zip_filename, filename=f"{brand_name}_Kit.zip", media_type="application/zip")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
