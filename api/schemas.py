from datetime import datetime
from typing import List
from pydantic import BaseModel

class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    post_id: int
    user_id: int
    date_created: datetime
    date_last_updated: datetime

    class Config:
        orm_mode = True

class PostPredictions(Post):
    major: float
    anger: float
    fear: float
    fun: float
    happy: float
    hate: float
    love: float
    neutral: float
    sadness: float
    worry: float

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    name:str = ""
    register_date: datetime
    posts : List[Post] = []

    class Config:
        orm_mode = True
