from fastapi import FastAPI
from .routers import company, employee, asset, asset_assign, company_sign, super_admin, login

app = FastAPI()


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