from fastapi import FastAPI

from app.apis.auth import router as auth_router
from app.apis.users import router as users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def home():
    return {"ok": True}
