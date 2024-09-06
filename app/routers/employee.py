from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, database, response
from ..security import get_current_user

router = APIRouter(tags=["Employees"])

@router.get("/companies/{company_id}/employees", response_model=List[response.EmployeeListResponse])
def get_employees(
    company_id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    if isinstance(current_user, models.Company) and current_user.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these employees"
        )
    
    employees = db.query(models.Employee).options(
        joinedload(models.Employee.company),
        joinedload(models.Employee.assignments)
    ).filter(models.Employee.company_id == company_id).all()
    return employees

@router.post("/companies/{company_id}/employees", response_model=response.EmployeeBase)
def add_employee(
    company_id: int, 
    employee: schemas.CreateEmployee, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    if isinstance(current_user, models.Company) and current_user.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add an employee to this company"
        )

    db_employee = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if db_employee:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee already exists")
    
    new_employee = models.Employee(**employee.dict(), company_id=company_id)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/employees/{id}", response_model=response.EmployeeListResponse)
def get_employee(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    employee = db.query(models.Employee).options(
        joinedload(models.Employee.company),
        joinedload(models.Employee.assignments)
    ).filter(models.Employee.id == id).first()
    
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    if isinstance(current_user, models.Company) and current_user.id != employee.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this employee"
        )

    return employee

@router.put("/employees/{id}", response_model=response.EmployeeListResponse)
def update_employee(
    id: int, 
    employee: schemas.UpdateEmployee, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    db_employee = db.query(models.Employee).filter(models.Employee.id == id)
    existing_employee = db_employee.first()
    
    if not existing_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    if isinstance(current_user, models.Company) and current_user.id != existing_employee.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this employee"
        )
    
    db_employee.update(employee.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_employee.first()

@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    db_employee = db.query(models.Employee).filter(models.Employee.id == id)
    existing_employee = db_employee.first()
    
    if not existing_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    if isinstance(current_user, models.Company) and current_user.id != existing_employee.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this employee"
        )
    
    db_employee.delete(synchronize_session=False)
    db.commit()
    return None
