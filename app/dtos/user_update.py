from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserUpdateDTO(BaseModel):
    """Data transfer object for user update requests.

    Attributes:
        name (str): Updated full name of the user.
            Must be between 1 and 100 characters.

        email (EmailStr): Updated email address for the user.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1, max_length=100)

    email: EmailStr
