from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str 
    content: str
    rating: Optional[int] = None
    published:bool = True

# connection to database should be in try/except 
while True:
    try :
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Es3131381', cursor_factory=RealDictCursor)
        # 'curser_factory=RealDictCursor' helps us to understand that witch 'data' maps to what 'column'
        cursor = conn.cursor()
        print("connection to database was seccesfull")
        break
    except Exception as error:
        print("connection to database failed!")
        print("Error: ",error)
        time.sleep(2)
        # Adding sleep method for delay

my_posts = [{"title":"the title of post 1","content":"content of post 1","id": 1},{"title":"the title of post 2","content":"content of post 2","id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None

@app.get("/")
def root():
    return {"Message":"Hello world"}

@app.post("/create_post")
def new_post(post:Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'response':new_post}

@app.get("/get_posts")
def getPosts():
    #بلافاصله بعد از دستور execute باید برای نمایش و برگشت اطلاعات از دستور fetchall استفاده کرد
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/posts/{id}")
def get_one_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id,{id} was not found"
        )
    return {"post" : post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail=f"post with id,{id} was not found")
    
    return {"deleted_post": deleted_post}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content=%s WHERE id = %s RETURNING *""",(post.title, post.content, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} has not been found!!")
    
    return {"data":updated_post}