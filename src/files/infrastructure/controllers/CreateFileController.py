from fastapi import status, UploadFile, File as FastAPIFile, Form
from fastapi.responses import JSONResponse
from src.files.application.CreateFileUseCase import CreateFileUseCase
from src.files.domain.entities.File import File
from src.files.domain.dto.FileResponse import CreateFileResponse, CreatedFileData
from src.core.cloudinary_service import get_cloudinary_service
from datetime import datetime
import os
import tempfile


class CreateFileController:
    def __init__(self, create_file: CreateFileUseCase):
        self.create_file = create_file
        self.cloudinary_service = get_cloudinary_service()

    async def execute(
            self,
            uploaded_by: int = Form(..., alias="uploadedBy"),
            file: UploadFile = FastAPIFile(...)
    ):
        try:
            if not file or not file.filename:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": "Debe proporcionar un archivo"}
                )

            file_extension = os.path.splitext(file.filename)[1].lower().replace('.', '')
            allowed_extensions = ['csv', 'xlsx', 'xls', 'xlsm']

            if file_extension not in allowed_extensions:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": f"Tipo de archivo no permitido. Solo se permiten: {', '.join(allowed_extensions)}"}
                )

            allowed_mime_types = [
                'text/csv',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/vnd.ms-excel.sheet.macroEnabled.12'
            ]

            if file.content_type not in allowed_mime_types:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": "Tipo MIME no permitido"}
                )

            file_content = await file.read()
            file_size = len(file_content)

            max_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_size:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": "Archivo muy grande. Máximo 10MB"}
                )

            temp_file_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                    temp_file.write(file_content)
                    temp_file_path = temp_file.name

                # Subir a Cloudinary
                result = self.cloudinary_service.upload_file(
                    temp_file_path,
                    folder="excel_files",
                    resource_type="raw"
                )

                file_public_id = result["public_id"]
                file_url = result["url"]

            finally:
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

            file_entity = File(
                file_name=file_public_id,
                original_name=file.filename,
                file_path=file_url,
                file_size=file_size,
                file_type=file_extension,
                uploaded_by=uploaded_by
            )

            saved_file = await self.create_file.execute(file_entity)

            response = CreateFileResponse(
                message="Archivo subido exitosamente",
                file=CreatedFileData(
                    fileId=saved_file.file_id,
                    fileName=saved_file.file_name,
                    originalName=saved_file.original_name,
                    filePath=saved_file.file_path,
                    fileSize=saved_file.file_size,
                    fileType=saved_file.file_type,
                    uploadedBy=saved_file.uploaded_by,
                    uploadDate=saved_file.upload_date.isoformat()
                )
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al subir archivo: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )