from fastapi import FastAPI, Depends, HTTPException, status
from models import Books
import database_models
from database import session, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Updated CORS to be more explicit for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://book-wormers.vercel.app", "http://localhost:3000"], 
    allow_methods=["*"],
    allow_headers=["*"]
)


# Create tables and seed data
database_models.Base.metadata.create_all(bind=engine)



# DATA IN FORM OF PYTHON LIST - Standardized to frontend 'ReadingStatus' type
books_seed = [
  Books(id=1, title="Ghost Town", author="Gaji Yaqub", genre="Fictional", status="want_to_read", description="Wonders of the Land of RageHole", pages=300, rating=5),
  Books(id=2, title="The Midnight Library", author="Matt Haig", genre="Fantasy", status="reading", description="Parallel universes exploration", pages=288, rating=4),
  Books(id=3, title="Dune", author="Frank Herbert", genre="Science Fiction", status="completed", description="Epic desert planet tale", pages=688, rating=5),
  Books(id=4, title="To Kill a Mockingbird", author="Harper Lee", genre="Classic", status="completed", description="Racial injustice and childhood innocence", pages=281, rating=5),
  Books(id=5, title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Classic", status="want_to_read", description="Wealth, love, and the American Dream", pages=180, rating=4),
  Books(id=6, title="Project Hail Mary", author="Andy Weir", genre="Science Fiction", status="reading", description="Space mission to save humanity", pages=476, rating=5),
  Books(id=7, title="The Silent Patient", author="Alex Michaelides", genre="Thriller", status="completed", description="Woman shoots husband, never speaks again", pages=336, rating=4),
  Books(id=8, title="Educated", author="Tara Westover", genre="Memoir", status="want_to_read", description="Survivalist family to education journey", pages=352, rating=4),
  Books(id=9, title="Atomic Habits", author="James Clear", genre="Self-Help", status="reading", description="Building good habits and breaking bad ones", pages=320, rating=5),
  Books(id=10, title="The Hobbit", author="J.R.R. Tolkien", genre="Fantasy", status="completed", description="Reluctant hobbit's unexpected adventure", pages=310, rating=5),
  Books(id=11, title="1984", author="George Orwell", genre="Dystopian", status="reading", description="Totalitarian regime and individual freedom", pages=328, rating=5),
  Books(id=12, title="Pride and Prejudice", author="Jane Austen", genre="Romance", status="completed", description="Love and social class in Regency England", pages=279, rating=4),
  Books(id=13, title="The Catcher in the Rye", author="J.D. Salinger", genre="Classic", status="want_to_read", description="Teenage rebellion and alienation", pages=277, rating=4),
  Books(id=14, title="Sapiens", author="Yuval Noah Harari", genre="Non-Fiction", status="reading", description="History of humankind from Stone Age to present", pages=443, rating=5),
  Books(id=15, title="The Lord of the Rings", author="J.R.R. Tolkien", genre="Fantasy", status="completed", description="Epic quest to destroy the One Ring", pages=1216, rating=5),
  Books(id=16, title="Neuromancer", author="William Gibson", genre="Science Fiction", status="dropped", description="Cyberpunk novel about artificial intelligence", pages=271, rating=3),
  Books(id=17, title="The Handmaid's Tale", author="Margaret Atwood", genre="Dystopian", status="want_to_read", description="Women's autonomy in patriarchal theocracy", pages=395, rating=5),
  Books(id=18, title="Becoming", author="Michelle Obama", genre="Memoir", status="reading", description="Life journey of former First Lady", pages=512, rating=5),
  Books(id=19, title="The Name of the Wind", author="Patrick Rothfuss", genre="Fantasy", status="completed", description="Musician and magician's origin story", pages=662, rating=4),
  Books(id=20, title="Thinking, Fast and Slow", author="Daniel Kahneman", genre="Psychology", status="want_to_read", description="Cognitive biases and decision making", pages=499, rating=4),
]

@app.on_event("startup")
def init_db():
    db = session()
    try:
        count = db.query(database_models.Books).count()
        if count == 0:
            for book in books_seed:
                db.add(database_models.Books(**book.model_dump()))
            db.commit()
    finally:
        db.close()




def get_db_session():
    db = session()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/books")
def get_books(db: Session = Depends(get_db_session)):
    db_books = db.query(database_models.Books).all()
    # ALWAYS return a list, even if empty. Never return a string here.
    return db_books

@app.get("/books/{id}")
def get_book_by_id(id: int, db: Session = Depends(get_db_session)):
    # .first() is required to get the actual data, not the query object
    book = db.query(database_models.Books).filter(database_models.Books.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return book

@app.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: Books, db: Session = Depends(get_db_session)):
    id_exists = db.query(database_models.Books).filter(database_models.Books.id == book.id).first()
    if id_exists:
        raise HTTPException(status_code=400, detail=f"Book with id {book.id} already exists")
    
    new_book = database_models.Books(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book # Return the object so frontend can update state

@app.put("/books/{id}")
def update_book(id: int, book: Books, db: Session = Depends(get_db_session)):
    db_book = db.query(database_models.Books).filter(database_models.Books.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Update fields
    update_data = book.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
        
    db.commit()
    db.refresh(db_book)
    return db_book # Frontend needs the updated object to refresh the UI

@app.delete("/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(database_models.Books).filter(database_models.Books.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Deleted successfully"} # Return JSON, not a plain string


