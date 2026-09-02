from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from sqlalchemy import func, or_, select
from typing import List

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)


#Show all posts
@router.get("/",
        response_model=List[schemas.Post_Votes])
def get_posts(db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user),
                limit: int = 10, search: str = ""):
  
  query = (
      select(models.Post, func.count(models.Vote.post_id).label("votes"))
      .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
      .group_by(models.Post.id)
      .where(or_(models.Post.title.contains(search), models.Post.content.contains(search)))
      .limit(limit)
  )
  posts_votes = db.execute(query).all()
  
  if not posts_votes:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="No posts Found")
  
  return posts_votes


#Add New Post
@router.post("/",
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

  new_post = models.Post(owner_id=current_user.id, **post.model_dump())

  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  
  return new_post


#Get Single Post
@router.get("/{id}",
        response_model=schemas.Post_Votes)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  query = (
      select(models.Post, func.count(models.Vote.post_id).label("votes"))
      .outerjoin(models.Vote, models.Vote.post_id == models.Post.id)
      .group_by(models.Post.id)
      .where(models.Post.id == id)
  )
  post = db.execute(query).first()
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  return post


#Delete a post
@router.delete("/{id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

  post = db.scalars(select(models.Post).where(models.Post.id == id)).first()
  
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform request action")
  
  db.delete(post)
  db.commit()
  
  return Response(status_code=status.HTTP_204_NO_CONTENT)


#Update Post
@router.put("/{id}",
        response_model=schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate,
                id: int,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  post = db.scalars(select(models.Post).where(models.Post.id == id)).first()
  
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform request action")
  
  for key, value in updated_post.model_dump().items():
    setattr(post, key, value)
    
  db.commit()
  db.refresh(post)

  return post
