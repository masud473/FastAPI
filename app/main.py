from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title:str
    content:str
    rating: float=None
    published:bool=True
my_posts=[{"title":'hi','content':'25','published':False,"id":1},
{"title":'hi','content':'25','rating':2.4,'published':False,"id":2}]
@app.get('/')
def read_root():
    return {'message': 'Hello World'}

@app.get('/')
def get_posts():
    return {'message': 'Hellos World'}

@app.get('/posts')
def get_posts():
    return {"data":my_posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict=post.dict()
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get('/posts/latest')
def get_latest_post():
    post=my_posts[-1]
    return {"data":post}

@app.get('/posts/{id}')
def get_post(id:int,response:Response):
    for i in my_posts:
        if i['id']==id:
            return {"data":i}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    post=None
    for i in my_posts:
        if i['id']==id:
            post=i
            break
    if post:
        my_posts.remove(post)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")

@app.put('/posts/{id}')
def update_post(id:int,post:Post):
    for i,p in enumerate(my_posts):
        if p['id']==id:
            my_posts[i]=post
            return {"data":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")