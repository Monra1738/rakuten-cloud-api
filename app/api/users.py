from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import get_current_user, revoke_tokens

import sqlite3

router = APIRouter(prefix="/users", tags=["Users"])


DB_PATH = "rakuten.db"


def test_example(tmp_path):
    test_db = tmp_path / "test.db"
    

@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):



    user = _get_user_from_db(current_user)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = {
        "user_id" : current_user,
        "information" : user
        }
    
    return response

    
@router.get("/{user_id}")
def get_user(
    user_id: str,
    current_user: str = Depends(get_current_user)
):
    
    user_info = _get_user_from_db(current_user)

    if user_info is None:
        raise HTTPException( status_code=404, detail="User not Found")
    
    role = user_info["role"]

    _role_validation(user_id, current_user, role, "get")


    user = _get_user_from_db(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    current_user: str = Depends(get_current_user)
):

    user = _get_user_from_db(current_user)

    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")

    role = user["role"]

    _role_validation(user_id, current_user, role, "delete")

    return _earse_user(user_id)

def _get_user_from_db(user_id : str):
    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute(
            """
            SELECT username, role
            FROM users
            WHERE user_id = ?
            """,
            (user_id, )
        )
        user = cursor.fetchone()
        if user is None: return None

        return { "username": user[0],
                "role": user[1]
                }
    
    finally:
        conn.close()

def _earse_user(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    try:

        cursor = conn.execute(
            """DELETE FROM users
            WHERE user_id = ?""", (user_id, )
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        conn.commit()
    except Exception:
        conn.rollback()
        raise
        
    finally:
        conn.close()

    revoke_tokens(user_id)

    message =  {
        "message": "User deleted successfully",
        "deleted_user_id": user_id
    }
    return message

def _role_validation(
    user_id: str,
    current_user: str,
    role: str,
    action: str
    ):
    if action not in ("get", "delete"):
        raise ValueError("Unsupported action")

    if role == "admin":
        return

    if role == "user":
        if user_id == current_user:
            return

    raise HTTPException(
        status_code=403,
        detail=f"You do not have permission to {action} this user"
    )