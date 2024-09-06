from typing import Union, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas, database, response
from ..security import get_current_user

router = APIRouter(tags=["Assets"])

@router.get("/companies/{company_id}/assets", response_model=List[response.AssetListResponse])
def get_assets(
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
            detail="Not authorized to access these assets"
        )
    
    assets = db.query(models.Asset).options(
        joinedload(models.Asset.company)
    ).filter(models.Asset.company_id == company_id).all()
    return assets

@router.post("/companies/{company_id}/assets", response_model=response.AssetBase, status_code=status.HTTP_201_CREATED)
def add_asset(
    company_id: int, 
    asset: schemas.CreateAsset, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    
    if isinstance(current_user, models.Company) and current_user.id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add an asset to this company"
        )
    
    new_asset = models.Asset(**asset.dict(), company_id=company_id)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

@router.get("/assets/{id}", response_model=response.AssetListResponse)
def get_asset(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    asset = db.query(models.Asset).options(
        joinedload(models.Asset.company)
    ).filter(models.Asset.id == id).first()
    
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    if isinstance(current_user, models.Company) and current_user.id != asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this asset"
        )
    
    return asset

@router.put("/assets/{id}", response_model=response.AssetListResponse)
def update_asset(
    id: int, 
    asset: schemas.UpdateAsset, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    db_asset = db.query(models.Asset).filter(models.Asset.id == id)
    existing_asset = db_asset.first()
    
    if not existing_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    if isinstance(current_user, models.Company) and current_user.id != existing_asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this asset"
        )
    
    db_asset.update(asset.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_asset.first()

@router.delete("/assets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(
    id: int, 
    db: Session = Depends(database.get_db), 
    current_user: Union[models.SuperAdmin, models.Company] = Depends(get_current_user)
):
    db_asset = db.query(models.Asset).filter(models.Asset.id == id)
    existing_asset = db_asset.first()
    
    if not existing_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    if isinstance(current_user, models.Company) and current_user.id != existing_asset.company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this asset"
        )
    
    db_asset.delete(synchronize_session=False)
    db.commit()
    return None
