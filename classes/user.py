# File containing User class. Run file to get user table in the database if it doesn't exist already

import sqlalchemy as sa
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class User(Base):
	__tablename__ = "users" 
	id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, unique=True)
	email = Column(String, nullable=False, unique=False)
	firstName = Column(String)
	lastName = Column(String)
	passwordHash = Column(String)
	avatar = Column(String)
	
# Create the engine: This creates the sql database with name 'PyProject'
engine = sa.create_engine("sqlite+pysqlite:///../assets/PyProject.db")

# Create the table if it doesn't exist
Base.metadata.create_all(engine)