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
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)
    return {'response':post_dict}

@app.get("/get_posts")
def getPosts():
    return my_posts

@app.get("/posts/{id}")
def get_one_post(id: int):
    post = find_post(id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id,{id} was not found"
        )
    return post

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT,
                            detail=f"post with id,{id} was not found")
    my_posts.pop(index)
    return {"Message":"The post has successfully been deleted"}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id={id} has not been found!!")
    my_posts[index] = post
    return {"data":post}