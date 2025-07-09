from fastapi import FastAPI
from pydantic import BaseModel
from azure.functions_fastapi import AzureFunctionsFastAPI

# Import your helper functions (assume these exist in /api folder or similar)
from api.openai_handler import get_openai_response
from api.cosmos_handler import insert_user_data
from api.storage_handler import upload_file

app = FastAPI(title="Nova AI Backend", description="API for Nova AI", version="1.0")

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

# Root test endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Nova AI backend!"}

# Chat route
@app.post("/chat")
def chat(req: ChatRequest):
    response = get_openai_response(req.prompt)
    return {"response": response}

# Store route
@app.post("/store")
def store(req: StoreRequest):
    result = insert_user_data(req.dict())
    return {"status": "success", "result": result}

# Upload route
@app.post("/upload")
def upload(req: UploadRequest):
    result = upload_file(req.filename, req.content)
    return {"status": "success", "result": result}

# Required to make FastAPI run on Azure Functions
main = AzureFunctionsFastAPI(app)
