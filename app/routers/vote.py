from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..database import get_db
from .. import oauth2, schemas, models


router = APIRouter(
  prefix="/votes",
  tags=["Votes"]
)

@router.post('/',
            status_code=status.HTTP_201_CREATED)
def add_vote(vote: schemas.Vote,
            db: Session = Depends(get_db),
            current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
  
  post = db.query(models.Post.id).filter(models.Post.id == vote.post_id).first()
  
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Post with id: {vote.post_id} Not Found")
    
  vote_query = db.query(models.Vote).filter(and_(models.Vote.post_id == vote.post_id,
                                          models.Vote.user_id == current_user.id))
  exist = vote_query.first()
  
  if vote.vote_dir == True:
    if exist:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                          detail=f"User Already vote this post")
    
    new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
    
    db.add(new_vote)
    db.commit()
    return {"message": "Vote added with success"}
  
  else:
    if exist is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Vote does not exist")

    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Vote removed with success"}


