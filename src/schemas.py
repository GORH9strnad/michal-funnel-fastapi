from pydantic import BaseModel

class Session(BaseModel):
    id: int
    token: str