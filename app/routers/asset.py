from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    tags=["Assets"]
)

@router.get("/companies/{company_id}/assets")
def get_assets(company_id: int, db: Session = Depends(database.get_db)):
    assets = db.query(models.Asset).filter(models.Asset.company_id == company_id).all()
    return assets

@router.post("/companies/{company_id}/assets", status_code=status.HTTP_201_CREATED)
def add_asset(company_id: int, asset: schemas.CreateAsset, db: Session = Depends(database.get_db)):
    new_asset = models.Asset(**asset.dict(), company_id=company_id)
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return new_asset

@router.get("/assets/{id}")
def get_asset(id: int, db: Session = Depends(database.get_db)):
    asset = db.query(models.Asset).filter(models.Asset.id == id).first()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return asset

@router.put("/assets/{id}")
def update_asset(id: int, asset: schemas.UpdateAsset, db: Session = Depends(database.get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == id)
    existing_asset = db_asset.first()
    if not existing_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    db_asset.update(asset.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return db_asset.first()

@router.delete("/assets/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_asset(id: int, db: Session = Depends(database.get_db)):
    db_asset = db.query(models.Asset).filter(models.Asset.id == id)
    existing_asset = db_asset.first()
    if not existing_asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    
    db_asset.delete(synchronize_session=False)
    db.commit()
    return None
