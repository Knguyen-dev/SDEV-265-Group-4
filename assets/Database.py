'''
0 Creates our sql database


'''
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserTable(Base):
    # Define the table's name
    __tablename__ = "users" 
    
	# Define the names of the columns, and then their types, and or attributes
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String, nullable=False, unique=True)
    email = sa.Column(sa.String, nullable=False, unique=False)
    firstName = sa.Column(sa.String)
    lastName = sa.Column(sa.String)
    passwordHash = sa.Column(sa.String)

# Create the engine: This creates the sql database with name 'PyProject'
engine = sa.create_engine("sqlite+pysqlite:///PyProject.db")

# Create the table if it doesn't exist
Base.metadata.create_all(engine)
