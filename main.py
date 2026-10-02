from fastapi import FastAPI, status, HTTPException, Depends
from typing import List
import models, schemas, utils
from database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"Message":"Hello world"}

@app.post("/create_post", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump()) #برای وارد کردن راحت تر تک تک پارامترهای entity
    db.add(new_post) #this adds the new post to the database
    db.commit() #this commits the changes to the database
    db.refresh(new_post) 
    
    return new_post

@app.get("/get_posts", response_model=List[schemas.Post])
def getPosts(db: Session = Depends(get_db)):
 
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id,{id} was not found"
        )
    return post

@app.delete("/posts/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(delete_post)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail=f"post with id,{id} was not found")
    
    return {"deleted_post": deleted_post}

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id={id} has not been found!!")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreate)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump()) #برای وارد کردن راحت تر تک تک پارامترهای entity
    db.add(new_user) #this adds the new user to the database
    db.commit() #this commits the changes to the database
    db.refresh(new_user) 
        
    return new_user

@app.get("/get_users", response_model=List[schemas.UserOut])
def getPosts(db: Session = Depends(get_db)):
 
    users = db.query(models.User).all()
    return users