"""models.py: Definition of classes for sqlalchemy"""

from datetime import date
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float, Text, Date
import database as _database

class User(_database.Base):
    """
        description

        params:


        returns:

    """

    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, default="empty")
    last_name = Column(String, default="empty")
    email = Column(String, unique=True)
    register_date = Column(Date, default=date.today())

    posts = relationship("Post", back_populates="owner")


class Post(_database.Base):
    """
        description

        params:


        returns:

    """

    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    date_created = Column(Date, default=date.today())
    date_last_updated=Column(Date, default=date.today())
    text = Column(Text)
    major = Column(String)
    anger = Column(Float)
    fear = Column(Float)
    fun = Column(Float)
    happy = Column(Float)
    hate = Column(Float)
    love = Column(Float)
    neutral = Column(Float)
    sadness = Column(Float)
    worry = Column(Float)

    owner = relationship("User", back_populates="posts")
