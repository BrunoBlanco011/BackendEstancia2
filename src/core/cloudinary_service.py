import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class CloudinaryService:
    _instance: Optional['CloudinaryService'] = None

    def __init__(self):
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET"),
            secure=True
        )

        print("Cloudinary configurado correctamente")

    def upload_file(self, file_path: str, folder: str = None, resource_type: str = "auto") -> dict:
        try:
            upload_folder = folder or os.getenv("CLOUDINARY_FOLDER", "transcriptor_materials")

            result = cloudinary.uploader.upload(
                file_path,
                folder=upload_folder,
                resource_type=resource_type
            )

            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
                "bytes": result.get("bytes")
            }
        except Exception as error:
            print(f"Error al subir archivo a Cloudinary: {error}")
            raise Exception(f"Failed to upload to Cloudinary: {str(error)}")

    def delete_file(self, public_id: str, resource_type: str = "image") -> bool:
        try:
            clean_public_id = public_id
            extensions = ['.pdf', '.PDF', '.jpg', '.JPG', '.jpeg', '.JPEG',
                          '.png', '.PNG', '.mp4', '.MP4', '.docx', '.DOCX',
                          '.pptx', '.PPTX', '.mp3', '.MP3', '.wav', '.WAV']
            for ext in extensions:
                clean_public_id = clean_public_id.replace(ext, '')

            result = cloudinary.uploader.destroy(clean_public_id, resource_type=resource_type)
            return result.get("result") == "ok"
        except Exception as error:
            print(f"Error al eliminar archivo de Cloudinary: {error}")
            return False

    def _ensure_extension(self, file_path: str) -> str:
        """Asegura que el file_path tenga extensión"""
        valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.mp4', '.docx',
                            '.pptx', '.mp3', '.wav', '.doc', '.txt']

        has_extension = any(file_path.lower().endswith(ext) for ext in valid_extensions)

        if not has_extension:
            return file_path

        return file_path

    def get_view_url(self, file_path: str, resource_type: str = "image") -> str:
        try:
            cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")

            if resource_type == "image":
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/{file_path}"
            elif resource_type == "video":
                return f"https://res.cloudinary.com/{cloud_name}/video/upload/{file_path}"
            else:
                file_path = self._ensure_extension(file_path)
                if any(file_path.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.pptx']):
                    return f"https://res.cloudinary.com/{cloud_name}/image/upload/fl_attachment:inline/{file_path}"
                else:
                    return f"https://res.cloudinary.com/{cloud_name}/raw/upload/{file_path}"
        except Exception as error:
            print(f"Error al obtener URL de visualización: {error}")
            return ""

    def get_download_url(self, file_path: str, resource_type: str = "image") -> str:
        try:
            cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
            file_path = self._ensure_extension(file_path)

            if resource_type == "video":
                return f"https://res.cloudinary.com/{cloud_name}/video/upload/fl_attachment/{file_path}"
            else:
                return f"https://res.cloudinary.com/{cloud_name}/image/upload/fl_attachment/{file_path}"
        except Exception as error:
            print(f"Error al obtener URL de descarga: {error}")
            return ""


def get_cloudinary_service() -> CloudinaryService:
    if CloudinaryService._instance is None:
        CloudinaryService._instance = CloudinaryService()
    return CloudinaryService._instance