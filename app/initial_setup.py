from sqlalchemy.orm import Session
from . import models, utils
from .config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_super_admin(db: Session):
    super_admin = db.query(models.SuperAdmin).filter(models.SuperAdmin.email == settings.super_admin_email).first()

    if not super_admin:
        hashed_password = utils.hash(settings.super_admin_password)
        new_super_admin = models.SuperAdmin(
            name=settings.super_admin_name,
            email=settings.super_admin_email,
            password=hashed_password
        )
        db.add(new_super_admin)
        db.commit()
        db.refresh(new_super_admin)
        print(f"Super admin {new_super_admin.email} created.")
    else:
        print("Super admin already exists.")
