from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    tags=["Employees"]
)

@router.get("/companies/{company_id}/employees")
def get_employees(company_id: int, db: Session = Depends(database.get_db)):
    employees = db.query(models.Employee).filter(models.Employee.company_id == company_id).all()
    return employees

@router.post("/companies/{company_id}/employees")
def add_employee(company_id: int, employee: schemas.CreateEmployee, db: Session = Depends(database.get_db)):
    new_employee = models.Employee(**employee.dict(), company_id=company_id)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/employees/{id}")
def get_employee(id: int, db: Session = Depends(database.get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

@router.put("/employees/{id}")
def update_employee(id: int, employee: schemas.UpdateEmployee, db: Session = Depends(database.get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == id)
    existing_employee = db_employee.first()
    if not existing_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    db_employee.update(employee.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_employee.first()

@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(database.get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == id)
    existing_employee = db_employee.first()
    if not existing_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    db_employee.delete(synchronize_session=False)
    db.commit()
    return None
