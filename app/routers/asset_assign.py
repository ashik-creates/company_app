from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from .. import models, schemas, database, response

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

@router.post("/{id}/assign", status_code=status.HTTP_201_CREATED)
def assign_asset(id: int, assignment: schemas.CreateAssetAssign, db: Session = Depends(database.get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id==assignment.employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="employee not found")

    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    existing_assignment = db.query(models.AssetAssign).filter(
        models.AssetAssign.asset_id == id,
        models.AssetAssign.employee_id == assignment.employee_id,
        models.AssetAssign.is_assigned == True
    ).first()

    if existing_assignment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset already assigned to this employee")

    new_assignment = models.AssetAssign(
        asset_id=id,
        employee_id=assignment.employee_id,
        assigned_at=assignment.assigned_at or datetime.utcnow(),
        is_assigned=True
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

@router.post("/{id}/unassign", status_code=status.HTTP_201_CREATED)
def unassign_asset(id: int, unassignment: schemas.UnassignAsset, db: Session = Depends(database.get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id==unassignment.employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="employee not found")
    
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    existing_assignment = db.query(models.AssetAssign).filter(
        models.AssetAssign.asset_id == id,
        models.AssetAssign.employee_id == unassignment.employee_id,
        models.AssetAssign.is_assigned == True
    ).first()

    if not existing_assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active assignment found for this asset and employee")

    new_unassignment = models.AssetAssign(
        asset_id=id,
        employee_id=unassignment.employee_id,
        returned_at=datetime.utcnow(),
        is_assigned=False
    )
    db.add(new_unassignment)
    db.commit()
    db.refresh(new_unassignment)
    return new_unassignment


@router.get("/{id}/history", response_model=response.AssetHistoryResponse)
def get_asset_history(id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).options(
        joinedload(models.Asset.assignments)
    ).filter(models.Asset.id == id).first()
    
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    return asset
