import sys
sys.path.insert(0, "../src/api")
sys.path.insert(0, "../src/utils")
from src.utils.CONST import API_PATH, EMAIL_ALREADY_EXISTS, SENTIMENTS
from src.utils.functions import predict
from src.api.database import Base
from src.api.services import get_db
from src.api.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
from numpy.random import uniform as u

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():

    email = "yahoo@mail.com"
    fn = "John"
    ln = "Doe"

    data = {
        'email': email,
        'first_name': fn,
        'last_name': ln
    }
    r = client.post(API_PATH + "/users/", json=data)

    assert r.status_code == 200, r.text
    res = r.json()
    if type(res) == str:
        assert res == EMAIL_ALREADY_EXISTS
    else:
        assert res["email"] == email
        assert res["first_name"] == fn
        assert res["last_name"] == ln
        assert "user_id" in res


def test_read_user():
    email = "yahoo@mail.com"
    fn = "John"
    ln = "Doe"

    user_id = 1
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["email"] == email
    assert res["first_name"] == fn
    assert res["last_name"] == ln
    assert res["user_id"] == user_id


def test_update_user():
    email = "google@google"
    fn = "Jane"
    ln = "Doe"

    data = {
        'email': email,
        'first_name': fn,
        'last_name': ln
    }

    r = client.put(API_PATH + "/users/1", params=data)
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["email"] == email
    assert res["first_name"] == fn
    assert res["last_name"] == ln


def test_create_post():
    prob = dict(zip(SENTIMENTS, [u() for _ in range(len(SENTIMENTS))]))
    text = "I'm so happy !"
    user_id = 1
    major = "happy"

    data = {
        'major': major,
        'text': text,
        **prob
    }
    r = client.post(API_PATH + f"/users/{user_id}/posts", json=data)
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["text"] == text
    assert res["major"] == "happy"

def test_read_post():
    text = "I'm so happy !"
    major = "happy"
    post_id = 1
    r = client.get(API_PATH + f"/posts/{post_id}")
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["text"] == text
    assert res["major"] == major


def test_update_post():
    text = "I'm so happy !"
    major = "happy"
    post_id = 1
    r = client.get(API_PATH + f"/posts/{post_id}")
    assert r.status_code == 200, r.text
    res = r.json()
    assert res["text"] == text
    assert res["major"] == major


def test_delete_post():
    post_id =1
    r = client.delete(API_PATH + f"/posts/{post_id}")
    res = r.json()
    assert res["message"] == f"successfully deleted post with id: {post_id}"


def test_delete_user():
    user_id = 1
    r = client.delete(API_PATH + f"/users/{user_id}")
    res = r.json()
    assert res["message"] == f"successfully deleted user with id: {user_id}"


def test_drop_db():
    drop_database(SQLALCHEMY_DATABASE_URL)
