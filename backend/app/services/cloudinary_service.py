import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from ..config import get_settings

settings = get_settings()

# Configure Cloudinary
if settings.cloudinary_url:
    cloudinary.config(cloudinary_url=settings.cloudinary_url)


async def upload_image(file: UploadFile, folder: str = "os-sistema") -> str:
    """
    Upload an image to Cloudinary
    
    Args:
        file: The uploaded file
        folder: Cloudinary folder name
        
    Returns:
        str: The secure URL of the uploaded image
    """
    try:
        # Read file content
        contents = await file.read()
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="image",
            quality="auto:good",
            fetch_format="auto"
        )
        
        return result["secure_url"]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer upload da imagem: {str(e)}"
        )


def delete_image(image_url: str) -> bool:
    """
    Delete an image from Cloudinary
    
    Args:
        image_url: The URL of the image to delete
        
    Returns:
        bool: True if successful
    """
    try:
        # Extract public_id from URL
        # Example URL: https://res.cloudinary.com/cloud/image/upload/v123/folder/image.jpg
        parts = image_url.split("/")
        if "upload" in parts:
            upload_idx = parts.index("upload")
            # public_id is everything after upload/v{version}/
            public_id = "/".join(parts[upload_idx + 2:]).rsplit(".", 1)[0]
            
            result = cloudinary.uploader.destroy(public_id)
            return result.get("result") == "ok"
    
    except Exception:
        return False
    
    return False
