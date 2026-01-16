from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Books(Base): # To have proper auth

  # Constructor
  __tablename__ = "Books"
  
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  author = Column(String)
  genre = Column(String)
  status = Column(String)
  description = Column(String)
  pages = Column(Integer)
  rating = Column(Integer)
  
  # Created_at
  # updated_at - yet to be implemented