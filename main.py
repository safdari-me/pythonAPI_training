from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
import models, schemas
from database import engine, SessionLocal, get_db 
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Connection to the database "without" the sqlalchemy
# connection to database should be in try/except 
# while True:
#     try :
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Es3131381', cursor_factory=RealDictCursor)
#         # 'curser_factory=RealDictCursor' helps us to understand that witch 'data' maps to what 'column'
#         cursor = conn.cursor()
#         print("connection to database was seccesfull")
#         break
#     except Exception as error:
#         print("connection to database failed!")
#         print("Error: ",error)
#         time.sleep(2)
        # Adding sleep method for delay

@app.get("/")
def root():
    return {"Message":"Hello world"}

@app.post("/create_post")
def new_post(post:schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.dict()) #برای وارد کردن راحت تر تک تک پارامترهای entity
    db.add(new_post) #this adds the new post to the database
    db.commit() #this commits the changes to the database
    db.refresh(new_post) 
    
    return {'response':new_post}

@app.get("/get_posts")
def getPosts(db: Session = Depends(get_db)):
    #بلافاصله بعد از دستور execute باید برای نمایش و برگشت اطلاعات از دستور fetchall استفاده کرد
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.get("/posts/{id}")
def get_one_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id,{id} was not found"
        )
    return {"post" : post}

@app.delete("/posts/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    db.delete(delete_post)
    db.commit()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail=f"post with id,{id} was not found")
    
    return {"deleted_post": deleted_post}

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s WHERE id = %s RETURNING *""",(post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id={id} has not been found!!")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data":post_query.first()} 