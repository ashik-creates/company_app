from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils
from ..security import get_current_user
from typing import Union

router = APIRouter(
    tags=["super_admin"]
)

@router.post("/create/super_admin")
def create_super_admin(
    admin: schemas.CreateSupAdmin, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, None] = Depends(get_current_user)
):
    if isinstance(current_user, models.SuperAdmin):
        db_admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.email == admin.email).first()
        if db_admin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin already exists")

        hashed_password = utils.hash(admin.password)
        admin.password = hashed_password
        new_admin = models.SuperAdmin(**admin.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create a Super Admin"
        )

@router.get("/admins")
def admins(
    db: Session = Depends(database.get_db),
    current_user: Union[models.SuperAdmin, None] = Depends(get_current_user)
):
    if isinstance(current_user, models.SuperAdmin):
        all_admins = db.query(models.SuperAdmin).all()
        return all_admins
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view admins"
        )
