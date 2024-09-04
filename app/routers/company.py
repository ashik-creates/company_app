from fastapi import APIRouter, Depends, HTTPException, status
from .. import database, models, schemas
from sqlalchemy.orm import Session

router = APIRouter(
    tags= ["companies"]

)

@router.get("/companies")
def get_companies(db:Session = Depends(database.get_db)):
    companies = db.query(models.Company).all()

    return companies

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, database, response

router = APIRouter()

@router.get('/company/{company_id}', response_model=response.CompanyDetail)
def get_company(company_id: int, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).options(
        joinedload(models.Company.employees),
        joinedload(models.Company.assets)
    ).filter(models.Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {company_id} not found"
        )
    
    return company


@router.put("/companies/{company_id}")
def update_company(company_id: int,company: schemas.UpdateCompany, db:Session = Depends(database.get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id)
    updated_company = db_company.first()
    if updated_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Company not found")
    db_company.update(company.dict(), synchronize_session=False)
    db.commit()
    return updated_company 

@router.delete("/companies/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int, db: Session = Depends(database.get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company_id)
    company_to_delete = db_company.first()

    if company_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Company not found")

    db_company.delete(synchronize_session=False)
    db.commit()
    return None