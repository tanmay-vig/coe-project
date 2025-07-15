# utils/file_handler.py

import os

def save_upload_file(uploaded_file, destination):
    with open(destination, "wb") as f:
        f.write(uploaded_file.file.read())

def ensure_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
