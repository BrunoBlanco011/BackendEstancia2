from pydantic import BaseModel, Field

class CreateFileRequest(BaseModel):
    uploaded_by: int = Field(..., ge=1, alias="uploadedBy")

    class Config:
        populate_by_name = True