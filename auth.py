import hashlib
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "rahul_super_secret_key_123"
ALGORITHM = "HS256"

# -------- Password Hash --------
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str):
    return hashlib.sha256(password.encode()).hexdigest() == hashed

# -------- JWT --------
def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])