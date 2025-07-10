import openai
import os
import re

openai.api_type = "azure"
openai.api_key = os.environ["AZURE_OPENAI_KEY"]
openai.api_base = os.environ["AZURE_OPENAI_ENDPOINT"]
openai.api_version = os.environ["AZURE_OPENAI_API_VERSION"]
deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT"]

def generate_code_files(prompt):
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "system", "content": "You are a full-stack AI developer. From the user prompt, generate:\n- HTML code\n- CSS code\n- JavaScript code\n- Python backend (Flask)\n- Additional route logic if needed."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response["choices"][0]["message"]["content"]

        # Extract different code blocks
        frontend_html = extract_code(content, "html")
        frontend_css = extract_code(content, "css")
        frontend_js = extract_code(content, "javascript")
        backend_app = extract_code(content, "python", match_first=True)
        backend_routes = extract_code(content, "routes", fallback=True)

        # Save files
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

        return True

    except Exception as e:
        print("❌ GPT-4 Error:", e)
        return False


def extract_code(text, keyword, match_first=False, fallback=False):
    """
    Extract code between ```<language> ... ``` or by keyword in comments
    """
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
