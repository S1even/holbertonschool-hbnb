#!/usr/bin/python3
from .base_model import BaseModel
import re


class User(BaseModel):
    def init(self, first_name: str, last_name: str, email: str, is_admin=False):
        super().init()
        self.first_name = self._validate_name(first_name, "First name", 50)
        self.last_name = self._validate_name(last_name, "Last name", 50)
        self.email = self._validate_email(email)
        self.is_admin = is_admin

    def _validate_name(self, name: str, field_name: str, max_length: int) -> str:
        """Validates that the name is not empty and within length limits."""
        if not name or len(name) > max_length:
            raise ValueError(f"{field_name} must be non-empty and less than {max_length} characters.")
        return name

    def _validate_email(self, email: str) -> str:
        """Validates the email address format."""
        email_format = r'^[\w.-]+@[\w.-]+.\w{2,4}$'
        if not re.match(email_format, email):
            raise ValueError("Invalid email format.")
        return email
