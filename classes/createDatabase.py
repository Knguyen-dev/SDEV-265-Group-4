from models import Base, User, Story, Message
from Database import engine

# Create the tables 
Base.metadata.create_all(bind=engine)