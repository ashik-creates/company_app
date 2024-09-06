from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import List, Union
from .. import models, schemas, database, response
from ..security import get_current_user

router = APIRouter(
    prefix="/assets",
    tags=["Asset Assignment"])

@router.post("/{id}/assign", status_code=status.HTTP_201_CREATED, response_model=response.AssetAssignDetail)
def assign_asset(
    id: int, 
    assignment: schemas.CreateAssetAssign, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    if isinstance(current_user, models.Company) and current_user.id != asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to assign this asset"
        )
    
    employee = db.query(models.Employee).filter(models.Employee.id == assignment.employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    existing_assignment = db.query(models.AssetAssign).filter(
        models.AssetAssign.asset_id == id,
        models.AssetAssign.is_assigned == True
    ).first()

    if existing_assignment:
        if existing_assignment.employee_id != assignment.employee_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset is already assigned to a different employee")
        else:
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


@router.post("/{id}/unassign", status_code=status.HTTP_200_OK, response_model=response.AssetAssignDetail)
def unassign_asset(
    id: int, 
    unassignment: schemas.UnassignAsset, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    assignment = db.query(models.AssetAssign).filter(
        models.AssetAssign.asset_id == id,
        models.AssetAssign.is_assigned == True
    ).order_by(models.AssetAssign.assigned_at.desc()).first()

    if not assignment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found or asset is not currently assigned")

    asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    if isinstance(current_user, models.Company) and current_user.id != asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to unassign this asset"
        )

    employee = db.query(models.Employee).filter(models.Employee.id == unassignment.employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    if assignment.returned_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset already returned")

    if assignment.employee_id != unassignment.employee_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Asset is not assigned to this employee")

    assignment.returned_at = datetime.utcnow()
    assignment.is_assigned = False
    db.commit()
    return assignment




@router.get("/{id}/assignments", response_model=List[response.AssetAssignDetail])
def get_assignments(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()

    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    if isinstance(current_user, models.Company) and current_user.id != asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these assignments"
        )

    assignments = db.query(models.AssetAssign).filter(models.AssetAssign.asset_id == id).all()
    return assignments

@router.get("/{id}/history", response_model=response.AssetHistoryResponse)
def get_asset_history(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    asset = db.query(models.Asset).options(
        joinedload(models.Asset.assignments)
    ).filter(models.Asset.id == id).first()

    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")

    if isinstance(current_user, models.Company) and current_user.id != asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this asset history"
        )
    
    return asset
