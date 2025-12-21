from sqlalchemy import create_engine #connection to base
from sqlalchemy.ext.declarative import declarative_base #base class for models
from sqlalchemy.orm import sessionmaker #sessions

from app.core.config import settings #Get DATABASE_URL from config.py

#Create connection
engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})

#Each request gets fresh session. All sessions use tasks.db
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class(parent class)
Base = declarative_base()

def get_db():
    db = Session() #new version for each request
    try:
        yield db #FastAPI
    finally:
        db.close()

if __name__ == "__main__":
    print("Database ok")
    print(f"engine: {settings.database_url}")
    