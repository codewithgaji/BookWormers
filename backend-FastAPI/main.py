from fastapi import FastAPI
from app.db.models import database_models
from app.db.database import engine, session
from app.db.schemas.models import BookCreate
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers.routers import authRouter

load_dotenv()

app = FastAPI()

# Updated CORS to be more explicit for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://book-wormers.vercel.app", "http://localhost:8080"], 
    allow_methods=["*"],
    allow_headers=["*"]
)


# Create tables and seed data
database_models.Base.metadata.create_all(bind=engine)



# DATA IN FORM OF PYTHON LIST - Standardized to frontend 'ReadingStatus' type
BOOKS_SEED = [
    BookCreate(title="Ghost Town", author="Gaji Yaqub", genre="Fictional", status="want_to_read", description="Wonders of the Land of RageHole", pages=300, rating=5),
    BookCreate(title="The Midnight Library", author="Matt Haig", genre="Fantasy", status="reading", description="Parallel universes exploration", pages=288, rating=4),
    BookCreate(title="Dune", author="Frank Herbert", genre="Science Fiction", status="completed", description="Epic desert planet tale", pages=688, rating=5),
    BookCreate(title="To Kill a Mockingbird", author="Harper Lee", genre="Classic", status="completed", description="Racial injustice and childhood innocence", pages=281, rating=5),
    BookCreate(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Classic", status="want_to_read", description="Wealth, love, and the American Dream", pages=180, rating=4),
    BookCreate(title="Project Hail Mary", author="Andy Weir", genre="Science Fiction", status="reading", description="Space mission to save humanity", pages=476, rating=5),
    BookCreate(title="The Silent Patient", author="Alex Michaelides", genre="Thriller", status="completed", description="Woman shoots husband, never speaks again", pages=336, rating=4),
    BookCreate(title="Educated", author="Tara Westover", genre="Memoir", status="want_to_read", description="Survivalist family to education journey", pages=352, rating=4),
    BookCreate(title="Atomic Habits", author="James Clear", genre="Self-Help", status="reading", description="Building good habits and breaking bad ones", pages=320, rating=5),
    BookCreate(title="The Hobbit", author="J.R.R. Tolkien", genre="Fantasy", status="completed", description="Reluctant hobbit's unexpected adventure", pages=310, rating=5),
    BookCreate(title="1984", author="George Orwell", genre="Dystopian", status="reading", description="Totalitarian regime and individual freedom", pages=328, rating=5),
    BookCreate(title="Pride and Prejudice", author="Jane Austen", genre="Romance", status="completed", description="Love and social class in Regency England", pages=279, rating=4),
    BookCreate(title="The Catcher in the Rye", author="J.D. Salinger", genre="Classic", status="want_to_read", description="Teenage rebellion and alienation", pages=277, rating=4),
    BookCreate(title="Sapiens", author="Yuval Noah Harari", genre="Non-Fiction", status="reading", description="History of humankind from Stone Age to present", pages=443, rating=5),
    BookCreate(title="The Lord of the Rings", author="J.R.R. Tolkien", genre="Fantasy", status="completed", description="Epic quest to destroy the One Ring", pages=1216, rating=5),
    BookCreate(title="Neuromancer", author="William Gibson", genre="Science Fiction", status="dropped", description="Cyberpunk novel about artificial intelligence", pages=271, rating=3),
    BookCreate(title="The Handmaid's Tale", author="Margaret Atwood", genre="Dystopian", status="want_to_read", description="Women's autonomy in patriarchal theocracy", pages=395, rating=5),
    BookCreate(title="Becoming", author="Michelle Obama", genre="Memoir", status="reading", description="Life journey of former First Lady", pages=512, rating=5),
    BookCreate(title="The Name of the Wind", author="Patrick Rothfuss", genre="Fantasy", status="completed", description="Musician and magician's origin story", pages=662, rating=4),
    BookCreate(title="Thinking, Fast and Slow", author="Daniel Kahneman", genre="Psychology", status="want_to_read", description="Cognitive biases and decision making", pages=499, rating=4),
]

@app.on_event("startup")
def init_db():
    db = session()
    try:
        count = db.query(database_models.Books).count()
        if count == 0:
            for book in BOOKS_SEED:
                db.add(database_models.Books(**book.model_dump()))
            db.commit()
    finally:
        db.close()





# --- ROUTES ---
app.include_router(authRouter)





@app.get("/")
def welcome_page():
    return {
        "Hello": "Welcome to Bookwormers-backend service😁"
}


