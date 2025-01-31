import base64
import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from urllib.parse import urlparse
from datetime import datetime
from app.core.config import SettingsDep

# Directory to save uploaded images
IMAGE_DIR = "../static/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

router = APIRouter()

@router.post("/upload-image")
async def upload_image(image: dict, settings: SettingsDep):
    base64_str = image.get("image")
    if not base64_str:
        raise HTTPException(status_code=400, detail="No image provided")

    # Decode and save the image
    image_data = base64.b64decode(base64_str.split(",")[1])
    filename = f"uploaded_image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(IMAGE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(image_data)

    # Return the public URL
    return {"url": f"{settings.APP_PROTOCOL}://{settings.APP_HOST}:{settings.APP_PORT}/{IMAGE_DIR}/{filename}"}


@router.delete("/delete-image")
async def delete_image(url: str):
    # Parse the URL to extract the path
    parsed_url = urlparse(url)
    filepath = parsed_url.path.lstrip("/") 
    if os.path.exists(filepath):
        os.remove(filepath)
        return {"message": "Image deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Image not found")