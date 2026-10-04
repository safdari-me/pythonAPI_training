from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from typing import List
import schemas,models

#برای اینکه مجبور نباشیم که هر جا /posts رو بنویسیم
router = APIRouter(
     prefix="/posts",
     tags=['posts']
)

@router.post("/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.model_dump()) #برای وارد کردن راحت تر تک تک پارامترهای entity
    db.add(new_post) #this adds the new post to the database
    db.commit() #this commits the changes to the database
    db.refresh(new_post) 
    
    return new_post

@router.get("/", response_model=List[schemas.Post])
def getPosts(db: Session = Depends(get_db)):
 
    posts = db.query(models.Post).all()
    return posts

@router.get("/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id,{id} was not found"
        )
    return post

@router.delete("/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(delete_post)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail=f"post with id,{id} was not found")
    
    return {"deleted_post": deleted_post}

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
   
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id={id} has not been found!!")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()