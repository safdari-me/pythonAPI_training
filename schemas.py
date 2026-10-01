from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str 
    content: str
    published:bool = True

class PostCreate(PostBase):
    pass

#در این بخش response schema مشخص میشه
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

