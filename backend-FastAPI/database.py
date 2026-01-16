from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



db_url = "postgresql://postgres:Universal1234@localhost/bookwormer"

engine = create_engine(db_url)

session = sessionmaker(auto_flush=False, auto_commit = False, bind=engine)