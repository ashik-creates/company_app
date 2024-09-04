from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, models, database, security, utils

router = APIRouter()

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.SuperAdmin).filter(
        models.SuperAdmin.email == user_credentials.username).first()

    if not user:
        
        user = db.query(models.Company).filter(
            models.Company.email == user_credentials.username).first()

    if not user:
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    
    user_type = "super_admin" if isinstance(user, models.SuperAdmin) else "company"

    access_token = security.create_access_token(data={"user_id": str(user.id), "user_type": user_type})

    return {"access_token": access_token, "token_type": "bearer"}
