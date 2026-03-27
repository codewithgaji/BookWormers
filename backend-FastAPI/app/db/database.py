from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() # This load the env environment variables
db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL Not Set")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)


# This ensures that the db does not autocommit. We want to control when commits happen, especially for seeding data and handling transactions in the future.
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit = False, bind=engine)



def get_db_session(): # this provides session access to the routers.
    db = session()
    try:
        yield db
    finally:
        db.close()