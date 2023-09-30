from fastapi import FastAPI, Depends
app=FastAPI()

import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

# this next line of code will create a todo.db file which means that databse is created successfully!
Base.metadata.create_all(engine)
def get_session():
    session= SessionLocal()
    try:
        yield session
    finally:
        session.close()

# fake database creation:-
fakeDatabase={
    1:{'task':'Clean Car'},
    2:{'task':'Clean deck'},
    3:{'task':'Clean new'}
}

# @app.get("/")
# def getItems():
#     # return ['Item 1', 'Item 2', 'Item3']
#     return fakeDatabase

# doing the above same thing but now using a database
@app.get("/")
def getItems(session: Session= Depends(get_session)):
    # return ['Item 1', 'Item 2', 'Item3']
    items= session.query(models.Item).all()
    return items

# the next line is used to get the values using specific id numbers
@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item= session.query(models.Item).get(id)
    return item


# @app.post("/")
# # this is one way to post but not useful if the item list is high that is if more parameters are required. hence we use pydantic and we create a file as schemas.py
# # def addItems(task:str):
# def addItems(item:schemas.Item):
#     newId=len(fakeDatabase.keys())+1
#     # fakeDatabase[newId]={"task": task}
#     fakeDatabase[newId]={"task": item.task}
#     return fakeDatabase

# doing the same thing but now using the sqlite database connection:-
@app.post("/")
def addItems(item:schemas.Item, session: Session = Depends(get_session)):
    item=models.Item(task= item.task)
    # add new data to the database
    session.add(item)
    # commit new changes
    session.commit()
    session.refresh(item)
    return item




# update the data
# @app.put("/{id}")
# def updateItem(id: int, item: schemas.Item):
#     fakeDatabase[id]['task'] = item.task
#     return fakeDatabase

@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObject= session.query(models.Item).get(id)
    itemObject.task= item.task
    session.commit()
    return itemObject


# delete the data
# @app.delete("/{id}")
# def deleteItem(id: int):
#     del fakeDatabase[id]
#     return fakeDatabase

@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject= session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'item has been deleted..'

