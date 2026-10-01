from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#آدرس postgres database باید اینجا وارد بشه 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Es3131381@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#every time that we want to work with api endpoints we call this function.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
