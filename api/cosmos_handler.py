import os
from azure.cosmos import CosmosClient

cosmos_uri = os.getenv("COSMOS_DB_URI")
cosmos_key = os.getenv("COSMOS_DB_KEY")
client = CosmosClient(cosmos_uri, credential=cosmos_key)

DB_NAME = "zentra-db"
CONTAINER_NAME = "users"

def insert_user_data(user_data):
    try:
        db = client.get_database_client(DB_NAME)
        container = db.get_container_client(CONTAINER_NAME)
        container.create_item(body=user_data)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
