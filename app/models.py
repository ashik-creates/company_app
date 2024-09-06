from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from .database import Base
from sqlalchemy.orm import relationship

class SuperAdmin(Base):
    __tablename__ = "super_admins"
    id = Column(Integer,nullable=False , primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class CompanyPending(Base):
    __tablename__ = 'companies_pending'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer,nullable=False , primary_key=True)
    company_name = Column(String, unique=True ,nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    employees = relationship("Employee", back_populates="company", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="company", cascade="all, delete-orphan")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)  

    company = relationship("Company", back_populates="employees")
    assignments = relationship("AssetAssign", back_populates="employees", cascade="all, delete-orphan")
    

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    company = relationship("Company", back_populates="assets")
    assignments = relationship("AssetAssign", back_populates="assets", cascade="all, delete-orphan")

class AssetAssign(Base):
    __tablename__ = 'asset_assignments'

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id', ondelete='CASCADE'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    returned_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_assigned = Column(Boolean, default=True)

    assets = relationship("Asset", back_populates="assignments")
    employees = relationship("Employee", back_populates="assignments") 
