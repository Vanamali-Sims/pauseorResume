# src/main.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
import uuid

from .preprocessing import extract_text
from .embedding import get_embedding
from .ranking import rank_resumes


app = FastAPI()

# In-memory storage for demonstration purposes.
# In production, consider a persistent database or a vector index (e.g., FAISS).
resume_embeddings = {}

@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    """
    Endpoint to upload a resume file.
    """
    file_extension = os.path.splitext(file.filename)[1]
    temp_filename = f"data/{uuid.uuid4()}{file_extension}"
    
    # Ensure the data directory exists.
    os.makedirs("data", exist_ok=True)
    
    # Save the uploaded file.
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text from the file.
    try:
        text = extract_text(temp_filename)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    
    # Compute the text embedding.
    embedding = get_embedding(text)
    
    # Save the embedding with a unique ID.
    resume_id = str(uuid.uuid4())
    resume_embeddings[resume_id] = embedding
    
    return {"resume_id": resume_id, "message": "Resume uploaded and processed successfully."}

@app.post("/match/")
async def match(job_description: str = Form(...)):
    """
    Endpoint to match a job description against stored resumes.
    """
    # Compute the embedding for the provided job description.
    job_embedding = get_embedding(job_description)
    
    # Rank resumes based on similarity.
    ranked = rank_resumes(job_embedding, resume_embeddings)
    
    return {"results": ranked}

if __name__ == "__main__":
    # Run the app with uvicorn for local development.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
