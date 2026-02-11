from pydantic import BaseModel

class ReplicateRequest(BaseModel):
    action: str
    key: str
    value: str | None = None

