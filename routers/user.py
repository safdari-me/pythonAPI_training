from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import schemas, models, utils

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump()) #برای وارد کردن راحت تر تک تک پارامترهای entity
    db.add(new_user) #this adds the new user to the database
    db.commit() #this commits the changes to the database
    db.refresh(new_user) 
        
    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def getusers(db: Session = Depends(get_db)):
 
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user with id={id} has not been found!!")

    return user