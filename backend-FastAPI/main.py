from fastapi import FastAPI, Depends
from models import Books
import database_models
from database import session, engine
from sqlalchemy.orm import Session


app = FastAPI()


# DB DUMP

def init_db():
  db = session() # First create a session
  count = db.query(database_models.Books).count()

  if count == 0:
    for book in books:
      db.add(database_models.Books(**book.model_dump()))

    db.commit()

init_db()


def get_db_session():
  try:
    db = session()
    yield db
  finally:
    db.close()
    


 # DATA IN FORM OF PYTHON LIST
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



database_models.Base.metadata.create_all(bind=engine) # Used To link the data to the db




# CREATE

@app.post("/book")
def add_book(book: Books, db: Session = Depends(get_db_session)): # This is used to parse the value of the parameter 'book' to the pydantic model 'Books'.

  id_exists = db.query(database_models.Books).filter(database_models.Books.id == book.id).first() # This is to check the Id against any ID available in the db.
  if not id_exists:
    new_book = database_models.Books(**book.model_dump())
    db.add(new_book)
    # books.append(book) # This appends/adds to the list of books that we have
    db.commit()
    db.refresh(new_book) # This updates new_book in memory
    return f"{book.title} Added Successfully"
  return f"Book with id {book.id} Already exists"




@app.get("/")
def get_books(db: Session = Depends(get_db_session)):
  db_books = db.query(database_models.Books).all()
  if not db_books:
    return "No books Found in the DB"
  return db_books


@app.get("/book/{id}")
def get_book_by_id(id: int, db: Session = Depends(get_db_session)):
  db_books = db.query(database_models.Books).all()
  for book in db_books:
    if book.id == id:
      return book
  return "Book Not Found"
  
  # for i in range(len(books)):
  #   if books[i].id == id:
  #     return books[i]
  # return "Book Not Found"




# UPDATE
@app.put("/book/{id}")
def update_book(book: Books, db: Session = Depends(get_db_session)):
  db_books = db.query(database_models.Books).filter(database_models.Books.id == book.id).first()
  if not db_books: # We run this to safely check for NONE so the db doesn't crash
    return f"Book {book.id} Not Found"
  
  # db_books.id = book.id       WE DON'T ACTUALLY SET PKs we only use them to find data in the db
  db_books.title = book.title
  db_books.author = book.author
  db_books.description = book.description
  db_books.genre = book.genre
  db_books.pages = book.pages
  db_books.status = book.status
  db_books.rating = book.rating
  db.commit()
  return f"Book {db_books.id} Updated Successfully"
  
  
  
  # for i in range(len(books)):
  #   if books[i].id == id:
  #     books[i] = book
  #     return "Book Updated Successfullly"
    
  # return "Book Not Found, and cannot be updated!"




# DELETE
@app.delete("/book")
def delete_book(id: int, db: Session = Depends(get_db_session)):
  db_books = db.query(database_models.Books).all()
  for book in db_books:
    if book.id == id:
      db.delete(book) 
      db.commit()
      return f"{book.title} has been Deleted from the DB Successfully"
  return "Book Not Found"
  





