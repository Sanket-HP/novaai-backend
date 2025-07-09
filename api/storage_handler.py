import os
from azure.storage.blob import BlobServiceClient

blob_conn_str = os.getenv("AZURE_STORAGE_CONNECTION")
blob_service = BlobServiceClient.from_connection_string(blob_conn_str)

CONTAINER_NAME = "zentra-files"

def upload_file(file_name, content):
    try:
        blob_client = blob_service.get_blob_client(container=CONTAINER_NAME, blob=file_name)
        blob_client.upload_blob(content, overwrite=True)
        return {"status": "uploaded"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
