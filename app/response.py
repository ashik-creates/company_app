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

class AssetAssignment(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    company_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class CompanyNameResponse(BaseModel):
    id: int
    company_name: str

    class Config:
        orm_mode = True

class EmployeeListResponse(BaseModel):
    id: int
    name: str
    email: str
    address: str
    company: CompanyNameResponse
    created_at: datetime

    class Config:
        orm_mode = True

class AssetResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    company_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class AssetListResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    company: CompanyNameResponse
    created_at: datetime

    class Config:
        orm_mode = True

class AssignmentHistory(BaseModel):
    id: int
    employee_id: int
    asset_id: int
    assigned_at: datetime
    returned_at: Optional[datetime]
    is_assigned: bool

    class Config:
        orm_mode = True

class AssetHistoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    company_id: int
    created_at: datetime
    assignments: List[AssignmentHistory]

    class Config:
        orm_mode = True

class AssetAssignDetail(BaseModel):
    id: int
    asset_id: int
    employee_id: int
    assigned_at: datetime
    returned_at: Optional[datetime] = None
    is_assigned: bool

    class Config:
        orm_mode = True

class PendingCompany(BaseModel):
    id: int
    company_name: str
    email: str
    address: str
    created_at: datetime

    class Config:
        orm_mode = True