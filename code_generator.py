import os
import re
from openai import AzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

# Initialize client
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)

deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT"]

def generate_code_files(prompt):
    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                ChatCompletionMessageParam(role="system", content=(
                    "You are a full-stack AI developer. From the user prompt, generate:\n"
                    "- HTML code\n- CSS code\n- JavaScript code\n- Python backend (Flask)\n- Additional route logic if needed."
                )),
                ChatCompletionMessageParam(role="user", content=prompt)
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content

        # Extract code
        frontend_html = extract_code(content, "html")
        frontend_css = extract_code(content, "css")
        frontend_js = extract_code(content, "javascript")
        backend_app = extract_code(content, "python", match_first=True)
        backend_routes = extract_code(content, "routes", fallback=True)

        os.makedirs("generated_projects/latest_project/frontend", exist_ok=True)
        os.makedirs("generated_projects/latest_project/backend", exist_ok=True)

        with open("generated_projects/latest_project/frontend/index.html", "w") as f:
            f.write(frontend_html or "<!-- No HTML generated -->")

        with open("generated_projects/latest_project/frontend/style.css", "w") as f:
            f.write(frontend_css or "/* No CSS generated */")

        with open("generated_projects/latest_project/frontend/app.js", "w") as f:
            f.write(frontend_js or "// No JS generated")

        with open("generated_projects/latest_project/backend/app.py", "w") as f:
            f.write(backend_app or "# No app.py code")

        with open("generated_projects/latest_project/backend/routes.py", "w") as f:
            f.write(backend_routes or "# No route logic")

        print("✅ Project generated successfully!")
        return True

    except Exception as e:
        import traceback
        print("❌ GPT-4 Error:", e)
        traceback.print_exc()
        return False


def extract_code(text, keyword, match_first=False, fallback=False):
    if not text:
        return ""

    if fallback:
        match = re.search(r"# routes\.py([\s\S]+?)(```|$)", text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    pattern = fr"```{keyword}([\s\S]+?)```"
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        return matches[0].strip() if match_first else "\n\n".join([m.strip() for m in matches])
    return ""
