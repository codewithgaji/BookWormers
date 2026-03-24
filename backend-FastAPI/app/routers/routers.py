from app.db.models.database_models import Books
from app.db.schemas.models import BookCreate
from app.db.models import database_models
from app.db.database import get_db_session
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi import APIRouter

authRouter = APIRouter()




@authRouter.get("/books")
def get_books(db: Session = Depends(get_db_session)):
    db_books = db.query(database_models.Books).all()
    # ALWAYS return a list, even if empty. Never return a string here.
    return db_books




@authRouter.get("/books/{id}") # This is a GET request, so we use the path parameter to specify the book ID
def get_book_by_id(id: int, db: Session = Depends(get_db_session)):
    # .first() is required to get the actual data, not the query object
    book = db.query(database_models.Books).filter(database_models.Books.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")
    return book





@authRouter.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: BookCreate, db: Session = Depends(get_db_session)):
    book_exists = db.query(database_models.Books).filter(database_models.Books.title == book.title).first()
    if book_exists:
        raise HTTPException(status_code=400, detail=f"Book with title '{book.title}' already exists")
    
    new_book = database_models.Books(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book # Return the object so frontend can update state



@authRouter.put("/books/{id}")
def update_book(id: int, book: BookCreate, db: Session = Depends(get_db_session)):
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



@authRouter.delete("/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db_session)):
    db_book = db.query(database_models.Books).filter(database_models.Books.id == id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Deleted successfully"} # Return JSON, not a plain string




