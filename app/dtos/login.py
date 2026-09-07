from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginDTO(BaseModel):
    """Data transfer object for user authentication requests.

    Attributes:
        email (EmailStr): A valid email address registered to the user account.
        password (str): The plain-text account password. Must be between 8 and 128 characters.
    """

    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
