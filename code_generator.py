import openai
import os
import re

# ✅ Load Azure OpenAI settings
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

def generate_code_files(prompt):
    try:
        print("📤 Prompt:", prompt)
        print("⚙️ Deployment:", deployment_name)
        print("🔐 API Key Set:", bool(openai.api_key))
        print("🌐 API Endpoint:", openai.api_base)

        # Check for required credentials
        if not all([openai.api_key, openai.api_base, openai.api_version, deployment_name]):
            print("❌ Missing Azure OpenAI environment variables.")
            return False

        # 🧠 Call Azure OpenAI GPT-4
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a full-stack AI developer. From the user prompt, generate:\n"
                        "- HTML code in ```html```\n"
                        "- CSS code in ```css```\n"
                        "- JavaScript in ```javascript```\n"
                        "- Python backend (Flask) in ```python```\n"
                        "- Additional Flask route logic in comment block marked with '# routes.py'"
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )

        content = response["choices"][0]["message"]["content"]
        print("✅ GPT-4 response received.")

        # Extract code blocks
        frontend_html = extract_code(content, "html")
        frontend_css = extract_code(content, "css")
        frontend_js = extract_code(content, "javascript")
        backend_app = extract_code(content, "python", match_first=True)
        backend_routes = extract_code(content, "routes", fallback=True)

        # Create folder structure
        os.makedirs("generated_projects/latest_project/frontend", exist_ok=True)
        os.makedirs("generated_projects/latest_project/backend", exist_ok=True)

        # Save frontend code
        with open("generated_projects/latest_project/frontend/index.html", "w", encoding="utf-8") as f:
            f.write(frontend_html or "<!-- No HTML generated -->")

        with open("generated_projects/latest_project/frontend/style.css", "w", encoding="utf-8") as f:
            f.write(frontend_css or "/* No CSS generated */")

        with open("generated_projects/latest_project/frontend/app.js", "w", encoding="utf-8") as f:
            f.write(frontend_js or "// No JS generated")

        # Save backend code
        with open("generated_projects/latest_project/backend/app.py", "w", encoding="utf-8") as f:
            f.write(backend_app or "# No app.py code")

        with open("generated_projects/latest_project/backend/routes.py", "w", encoding="utf-8") as f:
            f.write(backend_routes or "# No route logic")

        print("✅ Project files saved.")
        return True

    except Exception as e:
        import traceback
        print("❌ GPT-4 Error:", e)
        traceback.print_exc()
        return False


def extract_code(text, keyword, match_first=False, fallback=False):
    """
    Extract code from GPT-4 output using ```<keyword> ... ``` blocks
    or fallback to # routes.py comments
    """
    if not text:
        return ""

    if fallback:
        match = re.search(r"#\s*routes\.py([\s\S]+?)(```|$)", text, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    # Standard code block pattern: ```html ... ```
    pattern = fr"```{keyword}([\s\S]+?)```"
    matches = re.findall(pattern, text, re.IGNORECASE)

    if matches:
        return matches[0].strip() if match_first else "\n\n".join(m.strip() for m in matches)
    
    return ""
