from fastapi import FastAPI
from server.database import init_db

from server.routes.book import router as Router


app = FastAPI()
app.include_router(Router, tags=["Books"], prefix="/books")


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def index() -> dict:
    return {"message": "Welcome to your books app!"}
