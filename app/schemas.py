from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateCompany(BaseModel):
    company_name: str
    email: EmailStr
    password: str
    address: str

class UpdateCompany(BaseModel):
     company_name: Optional[str] = None
     address: Optional[str] = None
     email: Optional[str] = None

class CreateEmployee(BaseModel):
    name: str
    email: EmailStr
    address: str

class UpdateEmployee(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

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

class CreateSupAdmin(BaseModel):
    name: str
    email: EmailStr
    password: str  

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str
    user_type: str

class CreateCompanyPending(BaseModel):
    company_name: str
    email: str
    password: str    