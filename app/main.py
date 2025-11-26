from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import json
from app.logic import extract_text_from_pdf, analyze_cv

app = FastAPI(title="DocuMind API", version="1.0")

@app.post("/analyze-cv")
async def analyze_cv_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # 1. ფაილის დროებით შენახვა (რომ წაკითხვა შევძლოთ)
    temp_filename = f"temp_{file.filename}"
    
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. PDF-დან ტექსტის ამოღება (ვიძახებთ logic.py-ს)
        cv_text = extract_text_from_pdf(temp_filename)

        if not cv_text:
            return {"error": "PDF ფაილი ცარიელია ან ვერ წაიკითხა."}

        # 3. AI ანალიზი (ვიძახებთ logic.py-ს)
        analysis_result_str = analyze_cv(cv_text, job_description)
        
        # 4. სტრინგის გადაქცევა JSON ობიექტად
        analysis_json = json.loads(analysis_result_str)
        
        return analysis_json

    except Exception as e:
        return {"error": str(e)}

    finally:
        # 5. დროებითი ფაილის წაშლა (სისუფთავისთვის)
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.get("/")
def home():
    return {"message": "DocuMind API მუშაობს! გადადი /docs-ზე დოკუმენტაციის სანახავად."}