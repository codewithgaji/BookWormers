from pydantic import BaseModel

class Books(BaseModel): # To have proper auth
  id: int
  title: str
  author: str
  genre: str
  status: str
  description: str
  pages: int
  rating: int
  
  # Created_at
  # updated_at - yet to be implemented