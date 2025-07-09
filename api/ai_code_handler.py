import os
from openai import AzureOpenAI

# Azure OpenAI credentials
api_key = os.getenv("AZURE_OPENAI_KEY")
api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = "2025-01-01-preview"
deployment_name = "nova-gpt-4"

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_base,
)

def generate_code_from_prompt(prompt: str):
    try:
        system_prompt = (
            "You are an expert AI developer.\n"
            "When given a prompt, generate full frontend and backend code for a complete project.\n"
            "Respond with clearly labeled 'Frontend Code:' and 'Backend Code:' sections using triple backticks for code blocks."
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content

        return {
            "status": "success",
            "generated_code": content
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
