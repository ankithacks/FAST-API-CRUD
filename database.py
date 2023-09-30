# write these lines always to use sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# creates database engine...we specify the database type as sqlite
engine = create_engine('sqlite:///todo.db')
Base=declarative_base()
SessionLocal= sessionmaker(bind=engine, expire_on_commit=False)
# you have to write all these above lines of code in order to connect to the database


