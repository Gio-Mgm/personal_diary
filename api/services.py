from datetime import datetime
import sqlalchemy.orm as _orm
import database as _database
import models as _models
import schemas as _schemas

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

def create_user(db: _orm.Session, user: _schemas.UserCreate):
    db_user = _models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.User).offset(skip).limit(limit).all()



def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.user_id == user_id).first()


# --------------------- #
# ---- MSG QUERIES ---- #
# --------------------- #

def create_post(db: _orm.Session, post: _schemas.PostCreate, user_id: int):
    db_post = _models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: _orm.Session, skip: int, limit: int):
    return db.query(_models.Post).offset(skip).limit(limit).all()


def get_post(db: _orm.Session, post_id:int):
    return db.query(_models.Post).filter(_models.Post.post_id == post_id).first()


def delete_post(db: _orm.Session, post_id: int):
    db.query(_models.Post).filter(_models.Post.post_id == post_id).delete()
    db.commit()


def update_post(db: _orm.Session, post_id: int, post: _schemas.PostCreate):
    db_post = get_post(db=db, post_id=post_id)
    db_post.text = post.text
    db_post.date_last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return db_post
