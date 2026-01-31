from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db

router = APIRouter(
  prefix="/users",
  tags=['Users']
)

#Add User
@router.post("/",
          status_code=status.HTTP_201_CREATED,
          response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  
  #Hash the password - user.password
  hased_password = utils.hash(user.password)
  user.password = hased_password
  
  new_user = models.User(**user.dict())
  try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
  except IntegrityError:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail="Email already exist")
  
  return new_user


#get User with ID
@router.get("/{id}",
        response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

  user = db.query(models.User).filter(models.User.id == id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user with id: {id} was not found")
  
  return user
