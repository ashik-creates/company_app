from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, schemas, utils, security, response
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["company_signup"]
)

@router.post("/companies", response_model=response.PendingCompany)
def sign_up_company(company: schemas.CreateCompany, db: Session = Depends(database.get_db)):
    existing_company = db.query(models.CompanyPending).filter(
        (models.CompanyPending.company_name == company.company_name) | 
        (models.CompanyPending.email == company.email)
    ).first()

    if existing_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Company name or email already registered")

    hashed_password = utils.hash(company.password)
    company.password = hashed_password

    new_company = models.CompanyPending(**company.dict())
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return new_company

@router.get("/companies/pending/all", response_model=List[response.PendingCompany])
def get_pending_companies(
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(security.get_current_user)
):
    if not isinstance(current_user, models.SuperAdmin):
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="Not authorized to access pending companies"
    )

    pending_companies = db.query(models.CompanyPending).all()
    return pending_companies
    

@router.post("/companies/{company_id}/approve", response_model=response.CompanyBase)
def approve_company(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user: Union[models.SuperAdmin, models.Company] = Depends(security.get_current_user)
):
    if not isinstance(current_user, models.SuperAdmin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    pending_company = db.query(models.CompanyPending).filter(models.CompanyPending.id == company_id).first()

    if not pending_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    new_company = models.Company(
        company_name=pending_company.company_name,
        email=pending_company.email,
        password=pending_company.password,
        address=pending_company.address
    )
    db.add(new_company)
    db.delete(pending_company)
    db.commit()
    db.refresh(new_company)

    return new_company

@router.delete("/companies/{company_id}/reject")
def reject_company(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user: Union[models.SuperAdmin, models.Company] = Depends(security.get_current_user)
):
    if not isinstance(current_user, models.SuperAdmin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    pending_company = db.query(models.CompanyPending).filter(models.CompanyPending.id == company_id).first()

    if not pending_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    db.delete(pending_company)
    db.commit()

    return {"detail": "Company rejected"}    
