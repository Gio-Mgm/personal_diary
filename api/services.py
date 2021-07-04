"""services.py: Functions for creating queries."""

from datetime import date
import sqlalchemy.orm as _orm
from sqlalchemy.sql import func
from sqlalchemy import and_
import database as _database
import schemas as _schemas
import models as _models


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------- #
# ---- USER QUERIES ---- #
# ---------------------- #


def get_user(db: _orm.Session, user_id: int):
    """
        query get user
    """

    return db.query(_models.User).filter(_models.User.user_id == user_id).first()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    """
        query create user
    """

    db_user = _models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    print(f"db_user: {db_user}")
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: _orm.Session, user_id: int, user: _schemas.User):
    """
        query update user
    """

    db_user = get_user(db=db, user_id=user_id)
    db_user.email = user.email
    db_user.first_name = user.fn
    db_user.last_name = user.ln
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: _orm.Session, user_id: int):
    """
        query delete user
    """

    db.query(_models.User).filter(_models.User.user_id == user_id).delete()
    db.commit()


def get_users(db: _orm.Session, skip: int, limit: int):
    """
        query get all users
    """

    return db.query(_models.User).offset(skip).limit(limit).all()


def get_last_post(db: _orm.Session, user_id: int):
    """
        query get last user's post
    """

    return (db
        .query(_models.Post.text, _models.Post.date_last_updated)
        .filter(_models.Post.user_id == user_id)
        .order_by(_models.Post.date_last_updated.desc()).first()
    )



def get_post_by_date(db: _orm.Session, user_id: int, date: str, admin: bool):
    """
        query get a user post by date
    """

    if admin:
        return (db
                .query(_models.Post)
                .filter(_models.Post.user_id == user_id)
                .filter(_models.Post.date_last_updated == date)
                .first()
        )

    return (db
            .query(_models.Post.text)
            .filter(_models.Post.user_id == user_id)
            .filter(_models.Post.date_last_updated == date)
            .first()
    )


def get_user_posts(db: _orm.Session, user_id:int):
    """
        query get all posts from a user
    """

    return db.query(_models.Post).filter(_models.Post.user_id == user_id).all()


def get_post(db: _orm.Session, post_id: int):
    """
        query get post by id
    """

    return db.query(_models.Post).filter(_models.Post.post_id == post_id).first()


def create_post(db: _orm.Session, post: _schemas.PostCreate, user_id: int):
    """
        query create post
    """

    db_post = _models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: _orm.Session, post_id: int, post: _schemas.PostCreate):
    """
        query update post
    """

    db_post = get_post(db=db, post_id=post_id)
    db_post.major = post.major
    db_post.text = post.text
    db_post.worry = post.worry
    db_post.fear = post.fear
    db_post.neutral = post.neutral
    db_post.sadness = post.sadness
    db_post.hate = post.hate
    db_post.fun = post.fun
    db_post.happy = post.happy
    db_post.love = post.love
    db_post.anger = post.anger
    db_post.date_last_updated = date.today()
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: _orm.Session, post_id: int):
    """
        query delete post
    """

    db.query(_models.Post).filter(_models.Post.post_id == post_id).delete()
    db.commit()


def get_posts(db: _orm.Session, skip: int, limit: int):
    """
        query get all posts
    """

    return db.query(_models.Post).offset(skip).limit(limit).all()


def get_emails(db: _orm.Session):
    """
        query get list of emails
    """

    return db.query(_models.User.email).all()


def get_dates(db: _orm.Session, user_id: int):
    """
        query get list of dates from posts
    """

    return db.query(_models.Post.date_last_updated).filter(_models.Post.user_id == user_id).all()


def get_mean(db: _orm.Session, user_id: int, start: str, end: str):
    """
        query get mean of each sentiment
    """
    print(user_id == True)
    query = db.query(
        func.avg(_models.Post.anger).label('anger'),
        func.avg(_models.Post.sadness).label('sadness'),
        func.avg(_models.Post.love).label('love'),
        func.avg(_models.Post.happy).label('happy'),
        func.avg(_models.Post.fear).label('fear'),
        func.avg(_models.Post.worry).label('worry'),
        func.avg(_models.Post.neutral).label('neutral'),
        func.avg(_models.Post.hate).label('hate'),
        func.avg(_models.Post.fun).label('fun')
    ).filter(and_(
        _models.Post.date_last_updated >= start,
        _models.Post.date_last_updated <= end,
    ))
    
    if user_id:
        return query.filter(_models.Post.user_id == user_id).all()

    return query.all()
    

def check_posts_dates(db, start: str, end: str,  user_id: int):
    print(f"USER_ID : {user_id}")

    query = db.query(_models.Post).filter(and_(
        _models.Post.date_last_updated >= start,
        _models.Post.date_last_updated <= end,
    ))

    if user_id:
        return query.filter(_models.Post.user_id == user_id).count()

    return query.count()

