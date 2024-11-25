import re
from app.models.base_model import BaseModel
from app import bcrypt, db


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    @classmethod
    def create_user(cls, first_name, last_name, email, password, is_admin=False):
        """
        Method to create a new user.

        Validates the user's information and creates an entry in the database.
        
        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            email (str): User's email.
            password (str): User's password.
            is_admin (bool): Determines if the user is an admin (default: False).

        Returns:
            Instance of the User class.
        """

        first_name = cls.validate_name(first_name, "First")
        last_name = cls.validate_name(last_name, "Last")
        email = cls.validate_email(email)
        hashed_password = cls.hash_password(password)
        return cls(first_name=first_name, last_name=last_name, email=email, password=hashed_password, is_admin=is_admin)

    @staticmethod
    def validate_name(name, field_name):
        """
        Validates the name (first or last) to ensure it is not empty and does not exceed 50 characters.

        Args:
            name (str): The name to validate.
            field_name (str): The type of name ('First' or 'Last').

        Returns:
            str: The validated name.

        Raises:
            ValueError: If the name is empty or exceeds 50 characters.
        """

        if not name or len(name) > 50:
            raise ValueError("{} name must be provided and cannot exceed 50 characters.".format(field_name))

        return name

    @staticmethod
    def validate_email(email):
        """
        Validates the email format using a regular expression.

        Args:
            email (str): The email to validate.

        Returns:
            str: The validated email, or None if the format is invalid.
        """

        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.fullmatch(regex, email):
            return None

        return email


    @staticmethod
    def hash_password(password):
        """
        Hashes the password before storing it.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password, ready to be stored in the database.
        """

        return bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        """
        Verifies if the provided password matches the stored hashed password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the passwords match, False otherwise.
        """

        return bcrypt.check_password_hash(self.password, password)