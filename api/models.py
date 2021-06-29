''' Models for SQLAlchemy'''

from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float, Text, DateTime
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
    register_date = Column(DateTime, default=datetime.utcnow())

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
    date_created = Column(DateTime, default=datetime.now())
    date_last_updated = Column(DateTime, default=datetime.now())
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
