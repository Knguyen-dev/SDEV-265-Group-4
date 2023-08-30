import sys
sys.path.append("..") # easy way to go up one directory, allowing us to import more easily

from classes.user import User
myUser = User(
    username="john_doe",
    email="john@example.com",
    firstName="John",
    lastName="Doe",
    passwordHash="hashed_password",
    avatar="avatar_url"
)

print(myUser.username)