import os
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.cosmos import CosmosClient

# Custom Handlers
from api.openai_handler import get_openai_response
from api.cosmos_handler import insert_user_data, get_all_users
from api.storage_handler import upload_file
from api.project_generator import generate_project_from_prompt  # Make sure this file exists

# CosmosDB setup
cosmos_uri = os.getenv("COSMOS_DB_URI")
cosmos_key = os.getenv("COSMOS_DB_KEY")
client = CosmosClient(cosmos_uri, credential=cosmos_key)
DB_NAME = "nova-db"

# FastAPI app instance
app = FastAPI(
    title="Nova AI Backend",
    description="API for Nova AI - Chat, User Data Store, File Upload, and Project Generator",
    version="1.1.0"
)

# === Enable CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==== Request Models ====
class ChatRequest(BaseModel):
    prompt: str

class StoreRequest(BaseModel):
    name: str
    role: str
    github: str

class UploadRequest(BaseModel):
    filename: str
    content: str

class ProjectRequest(BaseModel):
    prompt: str

# ==== Endpoints ====

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Welcome to Nova AI backend!"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = get_openai_response(req.prompt)
    return {"response": response}

@app.post("/store")
def store(req: StoreRequest):
    result = insert_user_data(req.dict())
    return {"status": "success", "result": result}

@app.post("/upload")
def upload(req: UploadRequest):
    result = upload_file(req.filename, req.content)
    return {"status": "success", "result": result}

@app.get("/users")
def get_users():
    result = get_all_users()
    return {"status": "success", "result": result}

@app.post("/generate-project")
def generate_project(req: ProjectRequest):
    result = generate_project_from_prompt(req.prompt)
    return {"status": "success", "result": result}
