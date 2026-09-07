from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateDTO(BaseModel):
    """Data transfer object for user creation requests.

    Attributes:
        name (str): The full name of the user. Must be between 1 and 100 characters.
        email (EmailStr): A valid email address for the user.
        password (str): The plain-text password for the account. Must be between 8 and 128 characters.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
