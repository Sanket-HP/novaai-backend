from api.openai_handler import get_openai_response

def generate_project_from_prompt(prompt: str) -> dict:
    try:
        system_prompt = (
            "You are an AI Project Engineer. Based on the following user idea, "
            "generate a basic software project structure with:\n"
            "- Project Title\n"
            "- Folder Structure\n"
            "- Key files with sample code (brief only)\n"
            "- Technologies used\n"
            "- How to run\n\n"
            f"User Idea: {prompt}"
        )
        response = get_openai_response(system_prompt)
        return {"status": "success", "project": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
