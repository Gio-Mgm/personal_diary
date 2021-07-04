"""main.py: API endpoints definition"""

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas
from datetime import date

app = _fastapi.FastAPI()

_services.create_database()

@app.post("/users/")
def create_user(
    user: _schemas.UserCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for creating user
    """

    db_emails = _services.get_emails(db=db)
    emails = []
    for email in db_emails:
        emails.append(email[0])
    if user.email in emails:
        raise _fastapi.HTTPException(
            status_code=500, detail="email already in use")
    return _services.create_user(db=db, user=user)


@app.get("/users/")
def get_users(
    skip: int=0,
    limit: int=10,
    db: _orm.Session=_fastapi.Depends(_services.get_db)
):
    """
        Route for getting all users
    """

    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting a user
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(status_code=404, detail="This user does not exist")
    return db_user


@app.post("/users/{user_id}/posts")
def create_post(
    user_id: int,
    post: _schemas.PostCreate,
    db: _orm.Session=_fastapi.Depends(_services.get_db)
):
    """
        Route for creating post
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist")
    return _services.create_post(db=db, post=post, user_id=user_id)


@app.get("/users/{user_id}/posts")
def read_posts(
    user_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting all posts of a user
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist")
    return _services.get_user_posts(db=db, user_id=user_id)


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: _schemas.User,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    """
        Route for updating user
    """

    return _services.update_user(db=db, user=user, user_id=user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
        Route for deleting user
    """

    _services.delete_user(db=db, user_id=user_id)
    return {"message": f"successfully deleted user with id: {user_id}"}


@app.get("/users/{user_id}/last/")
def get_last_post(
    user_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting last user post
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist.")
    return _services.get_last_post(db=db, user_id=user_id)

@app.get("/posts/{user_id}/{date}/")
def get_post_by_date(
    user_id: int,
    admin: bool = False,
    date : str = str(date.today()),
    db:_orm.Session=_fastapi.Depends(_services.get_db)
):
    """
        Route for getting a user post from date
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist.")
    db_post = _services.get_post_by_date(
        db=db, user_id=user_id, date=date, admin=admin
    )
    if db_post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="No post on this date.")
    return db_post

@app.get("/posts/")
def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting all posts
    """

    posts = _services.get_posts(db=db,skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}")
def get_post(post_id: int, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    """
        Route for getting a post by its id
    """

    post = _services.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This post does not exist")
    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    """
        Route for deleting post
    """

    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"successfully deleted post with id: {post_id}"}


@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    post: _schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    """
        Route for editing post
    """

    return _services.update_post(db=db, post=post, post_id=post_id)

@app.get("/posts/{user_id}/dates")
def get_dates(
    user_id:int,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting dates of user's posts
    """

    return _services.get_dates(db=db,user_id=user_id)


@app.get("/posts/sentiments/")
def get_sentiments(
    start: str,
    end: str,
    user_id: int = None,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting user' mean emotion from date

    """
    count_db = _services.check_posts_dates(
        db=db, start=start, end=end, user_id=user_id
    )
    print(f"count_db : {count_db == True}")
    if count_db == 0:
        raise _fastapi.HTTPException(
            status_code=404, detail="No post for this interval")
    return _services.get_mean(db=db, start=start, end=end, user_id=user_id,)
