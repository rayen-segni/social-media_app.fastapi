from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#Algorithm
#Expriation time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes

def create_access_token(data: dict):
  
  to_encode = data.copy()
  
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
  
  to_encode.update({"exp": expire})
  
  token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return token


def verify_access_token(token: str, credentials_exeption):

  try:
    payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    id: str = payload.get("user_id")
    
    if not id :
      raise credentials_exeption

    token_data = schemas.TokenData(id=id)
    
  except JWTError:
    raise credentials_exeption
  
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme),
                    db: Session = Depends(database.get_db)):

  credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"})
  
  user_info = verify_access_token(token, credentials_exeption)
  
  return user_info

