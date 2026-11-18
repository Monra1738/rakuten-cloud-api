from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import get_current_user, revoke_tokens

import sqlite3

router = APIRouter(prefix="/users", tags=["Users"])

USERS = {
    "USER_A": {"username": "H", "role": "admin"},
    "USER_B": {"username": "V", "role": "user"},
    "USER_C": {"username": "S", "role": "guest"}
}



@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):

    if current_user not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    response = {
        "user_id" : current_user,
        "information" : USERS[current_user]
        }
    
    return response

    

@router.get("/{user_id}")
def get_user(user_id : str):
    conn = sqlite3.connect("rakuten.db")
    try:
        cursor = conn.execute(
            """SELECT username, role
               FROM users
               WHERE user_id = ? 
            """,
            (user_id, )
        )
        user = cursor.fetchone()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "username": user[0],
            "role" : user[1]
        }
    finally:
        conn.close()
    
def _earse_user(user_id: str):
    del USERS[user_id]
    revoke_tokens(user_id)

    message =  {
        "message": "User deleted successfully",
        "deleted_user_id": user_id
    }
    return message

@router.delete("/{user_id}")
def delete_user(user_id : str,
                current_user : str = Depends(get_current_user)):
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User to delete not found")

    if current_user not in USERS:
        raise HTTPException(status_code=404, detail="User not found")

    role = USERS[current_user]["role"]
    if role == "admin":
        message = _earse_user(user_id)
        return message
    
    elif role == "user":
        if user_id == current_user:
            message = _earse_user(user_id)
            return message
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to delte this user")

    elif role == "guest":
        raise HTTPException(status_code=403, detail="You do not have permission to delte this user")
    
    else:
        raise HTTPException(status_code=403, detail="PermissionError this user does do not have any role")
