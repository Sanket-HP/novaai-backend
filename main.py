from fastapi import FastAPI
from azure.functions import AsgiMiddleware

app = FastAPI()

@app.get("/docs-check")
def read_root():
    return {"message": "Swagger UI is working!"}

main = AsgiMiddleware(app)
