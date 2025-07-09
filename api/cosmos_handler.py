import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

# Load environment variables from a .env file if present (for local dev)
load_dotenv()

# Read Cosmos DB credentials from environment
cosmos_uri = os.getenv("COSMOS_DB_URI")
cosmos_key = os.getenv("COSMOS_DB_KEY")

# Initialize Cosmos DB client
client = CosmosClient(cosmos_uri, credential=cosmos_key)

# Define constants
DB_NAME = "nova-db"
CONTAINER_NAME = "users"
PARTITION_KEY_PATH = "/name"  # Must exist in your user data

# Ensure database and container exist
database = client.create_database_if_not_exists(id=DB_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path=PARTITION_KEY_PATH),
    offer_throughput=400
)

def insert_user_data(user_data: dict):
    try:
        container.create_item(body=user_data)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
