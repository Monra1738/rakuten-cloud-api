from fastapi import HTTPException, Header

TOKENS = {
    "token-admin-123": "USER_A",
    "token-user-456": "USER_B",
    "token-guest-789": "USER_C"
}

def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authorization")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Inavlid authorization scheme")

    token = authorization.split(' ', 1)[1] # Bearer token second...
    if token not in TOKENS:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return TOKENS[token]

def revoke_tokens(user_id : str):
    revoked_tokens = []
    for token_id, id_user in list(TOKENS.items()):
        if user_id == id_user: 
            del TOKENS[token_id] 
            revoked_tokens.append(token_id)
    
    return revoked_tokens
