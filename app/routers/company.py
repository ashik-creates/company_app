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

@router.get("/companies/{company_id}")
def read_company(company_id: int, db: Session = Depends(database.get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="Company not found")
    
    return company

@router.post("/companies")
def add_company(company: schemas.CreateCompany,db: Session = Depends(database.get_db)):
    new_company = models.Company(company_name= company.company_name,
                                 address= company.address)
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

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