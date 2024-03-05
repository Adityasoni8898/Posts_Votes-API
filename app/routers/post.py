from typing import List, Optional
from .. import schemas, models, oauth2
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(
        models.Post.owner_id == curr_user.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts
    
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    # return {"all_post":posts}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_item(post: schemas.PostCreate, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = curr_user.id, **post.model_dump()) #** means open the dictionary and pass the key value pairs as arguments
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #similar to RETURNING * in SQL
    
    return new_post
    
    # cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * ;""", (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"new post": new_post}

@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to view this post")
    else:
        return post
    
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s;""", (str(post_id),))
    # curr_post = cursor.fetchone()
    # if not curr_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # else:
    #     return {"post": curr_post}

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete this post")
    else: 
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *;""", (str(post_id),))
    # delete_post = cursor.fetchone()
    # if not delete_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # else:
    #     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to update this post")
    else: 
        post.update(**post.model_dump())
        db.commit()
        db.refresh(post)
        return post
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *;""", (post.title, post.content, str(post_id)))
    # updated_post = cursor.fetchone()
    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    # else:
    #     conn.commit()
    #     return {"post": updated_post}
