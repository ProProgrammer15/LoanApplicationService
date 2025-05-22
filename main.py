from fastapi import FastAPI
from app.interfaces.api import router
from app.infrastructure.database import create_tables


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_startup():
    create_tables()
    print("Tables created successfully.")