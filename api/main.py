"""main.py: API endpoints definition"""

import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas

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
def read_users(
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
def read_user(
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


@app.get("/users/{user_id}/post/")
def user_read_post(
    user_id: int,
    db:_orm.Session=_fastapi.Depends(_services.get_db)
):
    """
        Route for getting last user post
    """

    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="This user does not exist")
    return _services.get_user_post(db=db, user_id=user_id)

@app.get("/posts/")
def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting all posts
    """

    posts = _services.get_posts(db=db,skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}")
def read_post(post_id: int, db:_orm.Session = _fastapi.Depends(_services.get_db)):
    """
        Route for getting a post
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

@app.get("/users/{user_id}/by_dates")
def get_dates(
    user_id:int,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting dates of user's posts
    """

    return _services.get_dates(db=db,user_id=user_id)

@app.get("/users/{user_id}/by_dates/{date}")
def get_post_bydate(
    user_id: int,
    date: str,
    db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    """
        Route for getting user's post from date
    """

    return _services.get_user_post_bydate(user_id=user_id, db=db, date=date)
