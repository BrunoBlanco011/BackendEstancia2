from pydantic import BaseModel
from typing import Optional, List

class FileResponse(BaseModel):
    id: Optional[int]
    file_name: str
    original_name: str
    file_path: str
    file_size: int
    file_type: str
    uploaded_by: int
    upload_date: str

    @staticmethod
    def from_file(file):
        return FileResponse(
            id=file.file_id,
            file_name=file.file_name,
            original_name=file.original_name,
            file_path=file.file_path,
            file_size=file.file_size,
            file_type=file.file_type,
            uploaded_by=file.uploaded_by,
            upload_date=file.upload_date.isoformat() if file.upload_date else ""
        )


class FileListResponse(BaseModel):
    files: List[FileResponse]
    total: int


class SingleFileResponse(BaseModel):
    file: FileResponse


class CreatedFileData(BaseModel):
    fileId: Optional[int]
    fileName: str
    originalName: str
    filePath: str
    fileSize: int
    fileType: str
    uploadedBy: int
    uploadDate: str


class CreateFileResponse(BaseModel):
    message: str
    file: CreatedFileData


class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    error: str