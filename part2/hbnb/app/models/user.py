#!/usr/bin/python3
import re
import uuid


class User:
    def __init__(self, first_name, last_name, email):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

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
