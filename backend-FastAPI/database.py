from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


db_url = "postgresql://postgres:YxGgjkHPdMAcylcEpISwOwcProsVqHoU@shortline.proxy.rlwy.net:28916/railway"

if not db_url:
    raise RuntimeError("DATABASE_URL Not Set")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit = False, bind=engine)