from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from sqlalchemy import func ,or_
from ..schemas import List

router = APIRouter(
  prefix="/posts",
  tags=['Posts']
)


#Show all posts
@router.get("/",
        response_model=schemas.List[schemas.Post_Votes])
def get_posts(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user),
                limit: int = 10, search: str = ""):
  
  #Select normal post
  # posts = db.query(models.Post).filter(or_(
  #   models.Post.title.contains(search), models.Post.content.contains(search))).limit(limit).all()
  
  #Select post with id
  posts_votes = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
          .outerjoin(models.Vote)
          .group_by(models.Post.id)
          .filter(or_(models.Post.title.contains(search), models.Post.content.contains(search)))
          .limit(limit).all())
  
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
                current_user: int = Depends(oauth2.get_current_user)):

  new_post = models.Post(owner_id=current_user.id, **post.dict())

  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  
  return new_post


#Get Single Post
@router.get("/{id}",
        response_model=schemas.Post_Votes)
def get_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
  
  
  post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
          .outerjoin(models.Vote)
          .group_by(models.Post.id)
          .filter(models.Post.id == id)
          .first())
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  return post


#Delete a post
@router.delete("/{id}",
            status_code=status.HTTP_204_NO_CONTENT,)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):

  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  post = post_query.first()
  
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")


  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform request action")
  
  post_query.delete(synchronize_session=False)
  db.commit()
  
  return status.HTTP_204_NO_CONTENT


#Update Post
@router.put("/{id}",
        response_model=schemas.PostUpdate)
def update_post(updated_post: schemas.PostCreate,
                id: int,
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  post = post_query.first()
  if post is None :
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with id: {id} was not found")

  if post.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Not authorized to perform request action")
  
  post_query.update(updated_post.dict(), synchronize_session=False)
  db.commit()

  return post
