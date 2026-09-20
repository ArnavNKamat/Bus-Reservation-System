# models/user.py

class User:
    """
    Stores passenger information.
    """

    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self) -> dict:
        """
        Convert User object into dictionary for JSON storage.
        """
        return {
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create User object from JSON data.
        """
        return cls(
            data["name"],
            data["phone"],
            data["email"]
        )

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"Phone: {self.phone} | "
            f"Email: {self.email}"
        )