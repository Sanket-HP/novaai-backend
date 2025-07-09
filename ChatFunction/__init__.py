import azure.functions as func
import json

from ..api.openai_handler import get_openai_response
from ..api.cosmos_handler import insert_user_data
from ..api.storage_handler import upload_file

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        action = req_body.get("action")

        if action == "chat":
            prompt = req_body.get("prompt")
            result = get_openai_response(prompt)
            return func.HttpResponse(result)

        elif action == "store":
            data = req_body.get("data")
            result = insert_user_data(data)
            return func.HttpResponse(json.dumps(result), mimetype="application/json")

        elif action == "upload":
            file_name = req_body.get("filename")
            content = req_body.get("content")
            result = upload_file(file_name, content)
            return func.HttpResponse(json.dumps(result), mimetype="application/json")

        # Default case: invalid action
        return func.HttpResponse("Invalid action", status_code=400)

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
