import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "ahfihdasfadjhfnjjvusade"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        user_type: str = payload.get("user_type")
        if not (user_id and user_type in ["super_admin", "company"]):
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id, user_type=user_type)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(token, credentials_exception)

    if token_data.user_type == "super_admin":
        user = db.query(models.SuperAdmin).filter(models.SuperAdmin.id == token_data.id).first()
    elif token_data.user_type == "company":
        user = db.query(models.Company).filter(models.Company.id == token_data.id).first()
    else:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user
