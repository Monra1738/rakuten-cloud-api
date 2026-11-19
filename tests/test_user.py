from fastapi.testclient import TestClient
from app.main import app
from pytest import MonkeyPatch
from app.api import users as users_api
import sqlite3
from pathlib import Path 

client = TestClient(app)

def test_get_user_b():
    response = client.get("/users/USER_B",
                          headers={"Authorization": "Bearer token-user-456"})

    assert response.status_code == 200
    assert response.json() == {
        "username": "V", 
        "role": "user"
    }

def test_user_not_found():
    response = client.get("/users/USER_X",
                           headers={"Authorization": "Bearer token-admin-123"})
    assert response.status_code == 404

def test_get_me_without_token():
    response = client.get("/users/me")
                          
    assert response.status_code == 401

def test_get_me_with_valid_token():
    response = client.get("/users/me", 
                          headers={"Authorization": "Bearer token-user-456"})

    assert response.status_code == 200

def test_get_me_with_invalid_valid_token():
    response = client.get("/users/me", 
                          headers={"Authorization": "Bearer invalid-token"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid Token"}

def test_user_cannot_delete_another_user():
    response = client.delete(
        "/users/USER_A",
        headers={"Authorization": "Bearer token-user-456"}
    )

    assert response.status_code == 403



def test_user_cannot_view_another_user():
    response = client.get(
        "/users/USER_A",
        headers={"Authorization": "Bearer token-user-456"}
    )

    assert response.status_code == 403


def test_admin_can_delete(tmp_path: Path, monkeypatch: MonkeyPatch):

    test_db = tmp_path / "test.db"

    conn = sqlite3.connect(test_db)

    conn.execute("""
                CREATE TABLE users(
                user_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                role TEXT NOT NULL)
                """)

    conn.execute("""
                INSERT INTO users 
                VALUES(?, ?, ?)
                """, 
                ("USER_A", "H", "admin"))

    conn.execute("""
                INSERT INTO users VALUES (?, ?, ?)
                """, 
                ("USER_TEST", "Test", "user"))

    conn.commit()
    conn.close()

    monkeypatch.setattr(users_api, "DB_PATH", str(test_db))
    response = client.delete(
        "/users/USER_TEST",
        headers={"Authorization": "Bearer token-admin-123"}
    )

    assert response.status_code == 200

    conn = sqlite3.connect(test_db)

    cursor = conn.execute(
        "SELECT * FROM users WHERE user_id = ?",
        ("USER_TEST",)
    )

    user = cursor.fetchone()

    conn.close()

    assert user is None