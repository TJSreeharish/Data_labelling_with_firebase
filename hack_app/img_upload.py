import os
from firebase_admin import storage
from .check import initialize
import os
import shutil

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
            print(f"Successfully deleted the directory: {directory_path}")
        except OSError as e:
            print(f"Error: {e.strerror} - {directory_path}")
    else:
        print(f"Directory does not exist: {directory_path}")


def upload_images_in_directory(directory_path, firebase_base_path):
    initialize()
    bucket = storage.bucket()
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):  # Add other image extensions if needed
                local_path = os.path.join(root, file)
                # Get the relative path to preserve directory structure
                relative_path = os.path.relpath(local_path, directory_path)
                firebase_path = os.path.join(firebase_base_path, relative_path)
                
                # Upload the image
                blob = bucket.blob(firebase_path)
                blob.upload_from_filename(local_path)
                blob.make_public()
                print(f"Uploaded {file} to {blob.public_url}")
    
    delete_directory(directory_path)

def start():
# Usage
    directory_path = "./media/images"  # Local directory path containing images
    firebase_base_path = "images/"  # Base path in Firebase Storage (no need to include `gs://`)
    upload_images_in_directory(directory_path, firebase_base_path)
