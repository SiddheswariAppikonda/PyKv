from pydantic import BaseModel, Field

class SetRequest(BaseModel):
    key: str = Field(..., min_length=1, description="Key must not be empty")
    value: str = Field(..., min_length=1, description="Value must not be empty")

