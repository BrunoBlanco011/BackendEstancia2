from datetime import datetime
from typing import Optional

class File:
    def __init__(
        self,
        file_name: str,
        original_name: str,
        file_path: str,
        file_size: int,
        file_type: str,
        uploaded_by: int,
        file_id: Optional[int] = None,
        upload_date: Optional[datetime] = None
    ):
        self.file_id = file_id
        self.file_name = file_name
        self.original_name = original_name
        self.file_path = file_path
        self.file_size = file_size
        self.file_type = file_type  # 'csv', 'xlsx', 'xls', 'xlsm'
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date