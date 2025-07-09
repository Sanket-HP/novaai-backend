# api/ai_code_handler.py

from api.openai_handler import get_openai_response

def generate_code_from_prompt(prompt: str):
    try:
        # You can modify this prompt to include more structure if needed
        system_prompt = f"Write clean, well-structured code for the following task:\n\n{prompt}"
        response = get_openai_response(system_prompt)
        return {"status": "success", "code": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
