import zipfile
import os

def zip_generated_project():
    root_dir = "generated_projects/latest_project"
    zip_filename = "generated_project.zip"

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in filenames:
                full_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(full_path, root_dir)
                zipf.write(full_path, arcname=relative_path)

    print("📦 Project zipped at:", zip_filename)
