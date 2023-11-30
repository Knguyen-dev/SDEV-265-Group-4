from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text, Boolean
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    # Create attribute columns in the database
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(nullable=False)
    firstName:Mapped[str] = mapped_column(nullable=False)
    lastName:Mapped[str] = mapped_column(nullable=False)
    passwordHash:Mapped[str] = mapped_column(Text, nullable=False)
    avatar:Mapped[str] = mapped_column(nullable=False)

    '''
    1. Create 1 to many relationship between a User and their stories
    2. Allows us to access the stories linked with a User. So User.stories
    3. With back_populates, we prepare for Story.user, where we can access the 
        user linked with a story.
        
    cascade: For operations, adding, updating, deleting, merging, etc. If it's done to the user, then it
        must be done to all 'Story' objects linked to the user. So if you delete a User, then all of the 
        stories linked with that user are going to be deleted as well, which makes sense.

    delete-orphan: If an object is removed from a collection and it has no other references in the database (such as foreign keys pointing 
        to it), then that object is deleted since it has no relations. If a story is removed from a user, and that story object has no 
        other connections, it will be deleted from the database. This makes sense as when we only want stories in the database that 
        have are linked to a user. It has no use if it isn't linked.
    '''
    stories:Mapped[List["Story"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    

    def __repr__(self):
        return f"<User username={self.username}>"



class Story(Base):
    __tablename__ = "stories"
    id:Mapped[int] = mapped_column(primary_key=True)

    # The ID associated with the story
    userID:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    storyTitle:Mapped[str] = mapped_column(nullable=False)

    # Complete the relationship with the User 
    user:Mapped["User"] = relationship(back_populates="stories")

    
    
    '''
    - Create a 1 to many relationship between Story and Message. Since one story can have many messages, either from the user or ai
    
    cascade: If a story object is deleted, the messages are too. 
    delete-orphan: If a message isn't associated with a story or referenced anywhere else in the database
    , it's deleted from the database.
    
    '''
    messages:Mapped[List["Message"]] = relationship(back_populates="story", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Story title: {self.storyTitle}>"


class Message(Base):
    __tablename__ = "messages"
    id:Mapped[int] = mapped_column(primary_key=True)

    # Store the ID of the story that the message belongs to
    storyID:Mapped[int] = mapped_column(ForeignKey("stories.id"), nullable=False)
    
    isAISender:Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    # Store the text of the message
    text:Mapped[str] = mapped_column(Text, nullable=False)

    # Complete the 1 to many relationship between Story and Message
    # So through messages, we should be able to access the story.
    story:Mapped["Story"] = relationship(back_populates="messages") 

    def __repr__(self):
            return f"<Message Text: {self.text}>"


