from datetime import date
from typing import List
from pydantic import BaseModel

class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    major: str
    anger: float
    fear: float
    fun: float
    happy: float
    hate: float
    love: float
    neutral: float
    sadness: float
    worry: float
    pass

class Post(PostBase):

    date_last_updated: date
    user_id: int
    post_id: int
    date_created: date
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    first_name:str = ""
    last_name:str = ""

class User(UserBase):
    user_id: int
    register_date: date

    class Config:
        orm_mode = True
