from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_user_b():
    response = client.get("/users/USER_B")

    assert response.status_code == 200
    assert response.json() == {
        "username": "V", 
        "role": "user"
    }

def test_user_not_found():
    response = client.get("/users/USER_X")
    assert response.status_code == 404

def test_get_me_without_token():
    response = client.get("/users/me")
    assert response.status_code == 401

def test_get_me_with_valid_token():
    response = client.get("/users/me", 
                          headers={"Authorization": "Bearer token-user-456"})

    assert response.status_code == 200
