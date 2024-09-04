from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AssetBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    id: int
    name: str
    email: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True

class CompanyBase(BaseModel):
    id: int
    company_name: str
    email: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True

class CompanyDetail(CompanyBase):
    employees: List[EmployeeBase]
    assets: List[AssetBase]
