import os
import openai

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2025-01-01-preview"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

def get_openai_response(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            engine="nova-gpt-4",  # Your deployment name
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"OpenAI Error: {str(e)}"
