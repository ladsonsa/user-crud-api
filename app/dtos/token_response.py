from pydantic import BaseModel, ConfigDict


class TokenResponseDTO(BaseModel):
    """Data Transfer Object representing a successful token response payload.

    Configured with strict validation to forbid unexpected extra attributes.
    """

    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str
