from fastapi import FastAPI
from .routers import company, empoyee, asset

app = FastAPI()


app.include_router(company.router)
app.include_router(empoyee.router)
app.include_router(asset.router)


@app.get("/")
def root():
    return {"message": "hello world!"}