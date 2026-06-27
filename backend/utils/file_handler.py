import os, uuid
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file):
    if not allowed_file(file.filename):
        raise ValueError("Only PDF and DOCX files are allowed.")
    ext = file.filename.rsplit(".", 1)[-1].lower()
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], safe_name)
    file.save(path)
    return path, safe_name