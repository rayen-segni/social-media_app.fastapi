from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
  

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True, nullable=False)
  title = Column(String, nullable=False)
  content = Column(String, nullable=False)
  published = Column(Boolean, server_default='true', nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'))
  owner_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)

  owner = relationship("User")

class Vote(Base):
  __tablename__ = "votes"
  
  user_id = Column(Integer, ForeignKey(User.id, onupdate="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey(Post.id, onupdate="CASCADE"), primary_key=True)

