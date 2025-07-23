from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.database import Base
import pytest
import os

# Use an in-memory SQLite database for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user_success(db_session):
    response = client.post(
        "/users/",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password_hash" not in data 

def test_create_user_duplicate_username(db_session):
    client.post("/users/", json={"username": "testuser", "email": "test1@example.com", "password": "password123"})
    
    response = client.post("/users/", json={"username": "testuser", "email": "test2@example.com", "password": "password123"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_create_user_duplicate_email(db_session):
 
    client.post("/users/", json={"username": "user1", "email": "test@example.com", "password": "password123"})

    response = client.post("/users/", json={"username": "user2", "email": "test@example.com", "password": "password123"})
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_create_user_invalid_email(db_session):

    response = client.post("/users/", json={"username": "user1", "email": "not-an-email", "password": "password123"})
    assert response.status_code == 422 
def test_root_endpoint():
 
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Secure User API is running!"}