from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, database, response
from ..security import get_current_user
import traceback
from sqlalchemy.exc import IntegrityError
import logging

router = APIRouter(tags=["Companies"])

@router.get("/companies", response_model=List[response.CompanyDetail])
def get_companies(
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    if isinstance(current_user, models.SuperAdmin):
        companies = db.query(models.Company).options(
            joinedload(models.Company.employees),
            joinedload(models.Company.assets)
        ).all()
    elif isinstance(current_user, models.Company):
        companies = db.query(models.Company).options(
            joinedload(models.Company.employees),
            joinedload(models.Company.assets)
        ).filter(models.Company.id == current_user.id).all()

    return companies

@router.get('/companies/{company_id}', response_model=response.CompanyDetail)
def get_company(
    company_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    company = db.query(models.Company).options(
        joinedload(models.Company.employees),
        joinedload(models.Company.assets)
    ).filter(models.Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    if isinstance(current_user, models.Company) and current_user.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    return company

@router.put("/companies/{company_id}", response_model=response.CompanyBase)
def update_company(
    company_id: int,
    company: schemas.UpdateCompany, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).first()
    
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    if isinstance(current_user, models.Company) and current_user.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    db.query(models.Company).filter(models.Company.id == company_id).update(company.dict(), synchronize_session=False)
    db.commit()
    return db_company 

@router.delete("/companies/{company_id}", status_code=204)
def delete_company(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")

    if isinstance(current_user, models.SuperAdmin) or (isinstance(current_user, models.Company) and current_user.id == company_id):
        db.delete(company)
        db.commit()
    else:
        raise HTTPException(status_code=403, detail="Not authorized to delete this company")

    return None

