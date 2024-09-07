from fastapi import FastAPI
from .routers import company, employee, asset, asset_assign, company_sign, super_admin, login
from .database import SessionLocal
from .initial_setup import create_super_admin
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        create_super_admin(db)
    finally:
        db.close()


app.include_router(company.router)
app.include_router(employee.router)
app.include_router(asset.router)
app.include_router(asset_assign.router)
app.include_router(company_sign.router)
app.include_router(super_admin.router)
app.include_router(login.router)



@app.get("/")
def root():
    return {"message": "hello world!"}