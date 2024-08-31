from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CreateCompany(BaseModel):
    company_name: str
    address: str

class CreateCompany(BaseModel):
    company_name = Optional[str] = None
    address = Optional[str] = None

class CreateEmployee(BaseModel):
    name: str
    email: str
    address: str
    company_id: int

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    company_id: Optional[int] = None

class CreateAsset(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateAsset(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None    

class CreateAssetAssign(BaseModel):
    employee_id: int
    assigned_at: Optional[datetime] = None

class UnassignAsset(BaseModel):
    employee_id: int   
