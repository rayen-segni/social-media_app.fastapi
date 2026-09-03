from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  
  user = db.scalars(select(models.User).where(models.User.email == user_credentials.username)).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid credentials")
  
  if not utils.verify(user_credentials.password, user.password): #type: ignore
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid Credentials")
  
  access_token = oauth2.create_access_token(data={"user_id": user.id})

  return {"access_token": access_token, "token_type": "bearer"}
