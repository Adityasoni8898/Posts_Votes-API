from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

# making an model class

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/create_post/")
def create_item(post: Post):
    print(post)
    print(post.model_dump())
    return {"item": f"title: {post.title}, description: {post.content}"}

