from database import engine
import models
from fastapi import FastAPI
from database import SessionLocal

models.Base.metadata.create_all(bind=engine)

#Database session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.closee()

app=FastAPI()

@app.get("/")
async def get_todos(db):
    pass
