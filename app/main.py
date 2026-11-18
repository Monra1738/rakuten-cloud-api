##### ROLE BASE ACCES CONTORL ####

from fastapi import FastAPI
from app.api.users import router as users_router

app = FastAPI(title="Cloud Billing & acces API")
app.include_router(users_router)

@app.get("/health")
def health():
    return {"status" :  "ok"}

