from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



db_url = "postgresql://postgres:Universal1234@localhost/bookwormers"

engine = create_engine(db_url)

session = sessionmaker(autoflush=False, autocommit = False, bind=engine)