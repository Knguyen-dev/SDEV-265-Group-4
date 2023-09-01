# File that we'll import engine and session from

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
# Create an engine that'll setup a database in the assets folder
engine = create_engine("sqlite:///../assets/PyProject.db", echo=True)
session = Session(bind=engine)
