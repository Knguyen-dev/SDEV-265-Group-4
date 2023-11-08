
import sys
sys.path.append("..")


from classes.models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import copy

# Let's add some stories to my user
engine = create_engine("sqlite:///../assets/PyProject.db")
Session = sessionmaker(bind=engine)
session = Session()

target = session.query(User).filter_by(username="knguyensky42").first()
session.delete(target)
session.commit()