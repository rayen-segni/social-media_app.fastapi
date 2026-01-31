from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, List
from datetime import datetime

#Authentication

class UserLogin(BaseModel):
  email: EmailStr
  password: str
  

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[int] = None


#Users

class UserBase(BaseModel):
  email: EmailStr
  password: str

class UserCreate(UserBase):
  pass

class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime
  
  model_config = ConfigDict(from_attributes=True)


#Posts

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True


class PostCreate(PostBase): 
  pass

class PostUpdate(PostBase):
  created_at: datetime
  pass

class PostResponse(PostBase):
  id: int
  created_at: datetime
  owner: UserOut
  
  model_config = ConfigDict(from_attributes=True)
  # Here we show pydantic that the type of the data can be ORM model
  #After that pydantic will be able to acces to orm models an treat it 
  #Because pydantic natively just know how to treats python dictionnary 

class Vote(BaseModel):
  post_id: int
  vote_dir: bool


class Post_Votes(BaseModel):
  Post: PostResponse
  votes: int
