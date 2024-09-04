from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["super_admin"]
)

@router.post("/create/super_admin")
def create_super_admin(admin: schemas.CreateSupAdmin, db:Session = Depends(database.get_db)):
    db_admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.email==admin.email).first()
    if db_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail= "Admin already exist")
    hashed_password = utils.hash(admin.password)
    admin.password = hashed_password
    new_admin = models.SuperAdmin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.get("/admins")
def admins(db: Session = Depends(database.get_db)):
    all_admins = db.query(models.SuperAdmin).all()
    return all_admins