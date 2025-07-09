import os
import uuid
from azure.cosmos import CosmosClient

cosmos_uri = os.getenv("COSMOS_DB_URI")
cosmos_key = os.getenv("COSMOS_DB_KEY")
client = CosmosClient(cosmos_uri, credential=cosmos_key)

DB_NAME = "nova-db"
CONTAINER_NAME = "users"

def insert_user_data(user_data):
    try:
        # Ensure UUID is present
        if "id" not in user_data or not user_data["id"]:
            user_data["id"] = str(uuid.uuid4())

        db = client.get_database_client(DB_NAME)
        container = db.get_container_client(CONTAINER_NAME)

        response = container.create_item(body=user_data)
        return {"status": "success", "result": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_all_users():
    try:
        db = client.get_database_client(DB_NAME)
        container = db.get_container_client(CONTAINER_NAME)
        users = list(container.read_all_items())
        return {"status": "success", "result": users}
    except Exception as e:
        return {"status": "error", "message": str(e)}
