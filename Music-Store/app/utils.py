import os
from PIL import Image
from werkzeug.utils import secure_filename
from uuid import uuid4
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_cover_image(file):
    if file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    # ✅ secure & unique filename
    filename = secure_filename(file.filename)
    unique_name = f"{uuid4().hex}_{filename}"

    # ✅ absolute upload path
    upload_folder = os.path.join(current_app.root_path, "static", "uploads")

    # ✅ auto-create folder if missing
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, unique_name)

    # ✅ open image safely
    image = Image.open(file)

    # ✅ fix mode issues (important for JPEG)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # ✅ resize to fixed square
    image = image.resize((500, 500))

    # ✅ compress & save
    image.save(filepath, optimize=True, quality=75)

    return unique_name