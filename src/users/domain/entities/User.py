from datetime import datetime
from typing import Optional

class User:
    def __init__(
            self,
            name: str,
            last_name: str,
            email: str,
            password: str,
            role_id: int,
            user_id: int,
            registration_date: Optional[datetime] = None,
            profile_image: Optional[str] = None
    ):
            self.user_id = user_id
            self.name = name
            self.last_name = last_name
            self.email = email
            self.password = password
            self.role_id = role_id
            self.registration_date = registration_date
            self.profile_image = profile_image