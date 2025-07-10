from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from code_generator import generate_code_files
from zip_utils import zip_generated_project
import os

app = FastAPI(
    title="Nova AI App Builder",
    description="Generate a complete frontend and backend project using GPT-4",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/generate/")
async def generate(prompt: str = Form(...)):
    success = generate_code_files(prompt)
    if not success:
        return JSONResponse({"error": "Code generation failed"}, status_code=500)

    zip_generated_project()
    return JSONResponse({
        "message": "✅ Project generated successfully!",
        "download_url": "/download"
    })

@app.get("/download")
async def download_zip():
    return FileResponse("generated_project.zip", filename="generated_project.zip", media_type="application/zip")
