from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["company_signup"]
)

@router.post("/companies")
def sign_up_company(company: schemas.CreateCompany, db: Session = Depends(database.get_db)):

    existing_company = db.query(models.Company).filter(
        (models.Company.company_name == company.company_name) | 
        (models.Company.email == company.email)
    ).first()

    if existing_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Company name or email already registered")

    hashed_password = utils.hash(company.password)
    company.password = hashed_password

    new_company = models.Company(**company.dict())
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return new_company