from fastapi import FastAPI
from .routers import company, employee, asset, asset_assign

app = FastAPI()


app.include_router(company.router)
app.include_router(employee.router)
app.include_router(asset.router)
app.include_router(asset_assign.router)



@app.get("/")
def root():
    return {"message": "hello world!"}