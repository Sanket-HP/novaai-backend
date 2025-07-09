from fastapi import FastAPI
from pydantic import BaseModel
from azure.functions_fastapi import AzureFunctionsFastAPI

from api.openai_handler import get_openai_response
from api.cosmos_handler import insert_user_data
from api.storage_handler import upload_file

app = FastAPI(
    title="Nova AI Backend",
    description="API for Nova AI - Chat, User Data Store, File Upload",
    version="1.0.0"
)

# Request models
class ChatRequest(BaseModel):
    prompt: str

class StoreRequest(BaseModel):
    name: str
    role: str
    github: str

class UploadRequest(BaseModel):
    filename: str
    content: str

# Health check for Azure
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Nova AI backend!"}

# Chat with OpenAI
@app.post("/chat")
def chat(req: ChatRequest):
    response = get_openai_response(req.prompt)
    return {"response": response}

# Store user data to CosmosDB
@app.post("/store")
def store(req: StoreRequest):
    result = insert_user_data(req.dict())
    return {"status": "success", "result": result}

# Upload file to Azure Blob
@app.post("/upload")
def upload(req: UploadRequest):
    result = upload_file(req.filename, req.content)
    return {"status": "success", "result": result}

# Required for Azure Functions
main = AzureFunctionsFastAPI(app)
