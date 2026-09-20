# models/user.py

import hashlib
import secrets


class User:
    """
    Stores passenger and registered user account information.
    """

    def __init__(
        self,
        name: str,
        phone: str,
        email: str,
        password_hash: str = "",
        user_id: str = ""
    ):
        self.name = name.strip()
        self.phone = phone.strip()
        self.email = email.strip().lower()
        self.password_hash = password_hash
        self.user_id = user_id or f"USR-{secrets.token_hex(4).upper()}"

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256 with salt."""
        salt = "goa_express_bus_salt_"
        return hashlib.sha256((salt + password).encode()).hexdigest()

    def set_password(self, password: str):
        """Set user's hashed password."""
        self.password_hash = self.hash_password(password)

    def verify_password(self, password: str) -> bool:
        """Verify if provided password matches the hash."""
        if not self.password_hash:
            return False
        return self.password_hash == self.hash_password(password)

    def to_dict(self, include_private: bool = False) -> dict:
        """
        Convert User object into dictionary for JSON storage and API responses.
        """
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }
        if include_private:
            data["password_hash"] = self.password_hash
        return data

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create User object from JSON data.
        """
        return cls(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            email=data.get("email", ""),
            password_hash=data.get("password_hash", ""),
            user_id=data.get("user_id", "")
        )

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"Phone: {self.phone} | "
            f"Email: {self.email}"
        )