from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserUpdateDTO(BaseModel):
    """Data transfer object for user update requests.

    Attributes:
        name (str | None): Optional updated full name of the user. If provided,
            must be between 1 and 100 characters. Defaults to None.
        email (EmailStr | None): Optional updated email address for the user.
            Defaults to None.
    """

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None