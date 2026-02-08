from pydantic import BaseModel, Field

class Post(BaseModel):
    userId : int = Field(...,ge=1)
    id: int = Field(...,ge=1)
    title: str = Field(...,min_length=1)
    body: str = Field(...,min_length=1)
