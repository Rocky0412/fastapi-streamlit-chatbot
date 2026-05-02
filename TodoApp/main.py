from database import engine
import models
from fastapi import FastAPI,Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos
from fastapi import HTTPException,status,Path
from pydantic import BaseModel,Field
from typing import Annotated,Optional

models.Base.metadata.create_all(bind=engine)

#Database session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodosRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str
    priority:int =Field(gt=0,lt=6)
    completed:bool =Field(description="True or False")

app=FastAPI()

db_dependency=Annotated[Session,Depends(get_db)]

@app.get("/")
async def get_todos(db:db_dependency):
    return db.query(Todos).all()

@app.get("/{id}",status_code=status.HTTP_200_OK)
async def get_todo(db:db_dependency,id:int=Path(gt=0)):
    model= db.query(Todos).filter(Todos.id==id).first()
    if model:
        return {"message":model,"code":status.HTTP_200_OK}
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

async def create_todo(todo: TodosRequest, db: Session = db_dependency):

    new_todo = Todos(**todo.model_dump())

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int, todo: TodosRequest, db: db_dependency):

    existing_todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )

    # Update all fields
    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.priority = todo.priority
    existing_todo.completed = todo.completed

    db.commit()
    db.refresh(existing_todo)

    return existing_todo


@app.delete("/{id}",status_code=status.HTTP_200_OK)
async def deleteTodo(db:db_dependency,id:int=Path(gt=0)):
    model=db.query(Todos).filter(Todos.id==id).first()
    if not model:
        HTTPException(status_code=404,detail="Not found")
    db.delete(model)
    db.commit()
    return {"message":f"deleted {status.HTTP_200_OK}","data":model}
