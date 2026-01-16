from fastapi import FastAPI
from models import Books
import database_models
from database import session, engine

app = FastAPI()



books = [
  Books(id=1, title="Ghost Town", author="Gaji Yaqub", genre="Fictional", status="Want To Read", description="Wonders of the Land of RageHole, a Kingdom filled with lots of paradoxical events", pages=300, rating=5),
  
  Books(id=2, title="The Midnight Library", author="Matt Haig", genre="Fantasy", status="Reading", description="A woman explores different versions of her life across parallel universes", pages=288, rating=4),

  Books(id=3, title="Dune", author="Frank Herbert", genre="Science Fiction", status="Completed", description="An epic tale of politics, religion, and ecology on the desert planet Arrakis", pages=688, rating=5),

  Books(id=4, title="To Kill a Mockingbird", author="Harper Lee", genre="Classic", status="Completed", description="A gripping tale of racial injustice and childhood innocence in the American South", pages=281, rating=5),

  Books(id=5, title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Classic", status="Want To Read", description="A story of wealth, love, and the American Dream in the Jazz Age", pages=180, rating=4),

  Books(id=6, title="Project Hail Mary", author="Andy Weir", genre="Science Fiction", status="Reading", description="An astronaut must save humanity by traveling through space on a daring mission", pages=476, rating=5),

  Books(id=7, title="The Silent Patient", author="Alex Michaelides", genre="Thriller", status="Completed", description="A woman shoots her husband and never speaks again, captivating a psychotherapist", pages=336, rating=4),

  Books(id=8, title="Educated", author="Tara Westover", genre="Memoir", status="Want To Read", description="A memoir about a woman who leaves her survivalist family to pursue education", pages=352, rating=4),

  Books(id=9, title="Atomic Habits", author="James Clear", genre="Self-Help", status="Reading", description="Practical strategies for building good habits and breaking bad ones", pages=320, rating=5),

  Books(id=10, title="The Hobbit", author="J.R.R. Tolkien", genre="Fantasy", status="Completed", description="A reluctant hobbit embarks on an unexpected adventure to reclaim treasure from a dragon", pages=310, rating=5)
         ]






@app.get("/")
def get_books():
  return books

@app.get("/book/{id}")
def get_book_by_id(id: int):
  for i in range(len(books)):
    if books[i].id == id:
      return books[i]
  return "Book Not Found"


@app.put("/book")
def update_book(id: int, book: Books):
  for i in range(len(books)):
    if books[i].id == id:
      books[i] = book
      return "Book Updated Successfullly"
    
  return "Book Not Found, and cannot be updated!"

@app.delete("/book")
def delete_book(id: int):
  for i in range(len(books)):
    if books[i].id == id:
      del books[i]
      return "Book Deleted Successfully"
  
  return "Book Not Found"


@app.post("/book")
def add_book(book: Books): # This is used to parse the value of the parameter 'book' to the pydantic model 'Books'.
  books.append(book) # This appends/adds to the list of books that we have
  return f"{book.title} Added Successfully"
