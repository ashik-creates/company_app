from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from .database import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer,nullable=False , primary_key=True)
    company_name = Column(String, unique=True ,nullable=False)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    assets = relationship("Asset", back_populates="company")
    employees = relationship("Employee", back_populates="company") 

class Employee(Base):
    __tabelname__ = "employees"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    employees = relationship("Company", back_populates="employee") 
    assignments = relationship("AssetAssign", back_populates="employee") 
    

class Asset(Base):
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    company = relationship("Company", back_populates="asset") 
    assignments = relationship("AssetAssign", back_populates="asset")

class AssetAssign(Base):
    __tablename__ = 'asset_assignments'

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id', ondelete='CASCADE'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)

    asset = relationship("Asset", back_populates="assignments")
    employee = relationship("Employee", back_populates="assignments")    
