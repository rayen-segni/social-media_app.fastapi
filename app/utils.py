# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash(password: str):
#   return pwd_context.hash(password)

# def verify(plain_password, hashed_password):
#   return pwd_context.verify(plain_password, hashed_password)

import bcrypt

def hash(password: str) -> str:
    """Hash a password using bcrypt"""
    # Convert password to bytes and generate hash
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Return as string for storage
    return hashed.decode('utf-8')

def verify(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password"""
    pwd_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)
