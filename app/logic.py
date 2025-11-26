import os
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

# გარემოს ცვლადების (API Key) წაკითხვა .env ფაილიდან
load_dotenv()

# OpenAI კლიენტის შექმნა
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file_path: str):
    """
    ეს ფუნქცია კითხულობს PDF ფაილს და აბრუნებს სუფთა ტექსტს.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def analyze_cv(cv_text: str, job_description: str):
    """
    ეს ფუნქცია აგზავნის მონაცემებს OpenAI-თან და ითხოვს შეფასებას JSON ფორმატში.
    """
    
    prompt = f"""
    You are an expert HR AI Assistant. 
    Compare the following Candidate CV with the Job Description.
    
    JOB DESCRIPTION:
    {job_description}
    
    CANDIDATE CV:
    {cv_text}
    
    Provide a response in strict JSON format with the following keys:
    - match_score: (integer between 0-100)
    - missing_skills: (list of strings, technical skills from JD that are missing in CV)
    - summary: (string, brief explanation of the decision)
    - recommendation: (string, advice for the candidate)
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ან gpt-3.5-turbo, თუ gpt-4 არ გაქვს
            messages=[
                {"role": "system", "content": "You are a helpful HR assistant that outputs JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # ეს გარანტიას გვაძლევს, რომ პასუხი JSON იქნება
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error connecting to AI: {e}"