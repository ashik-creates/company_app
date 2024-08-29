from fastapi import APIRouter

router = APIRouter(
    prefix= "/companies",
    tags= ["company_api"]

)

@router.get("/companies")
def get_companies():
    return {"all"}

@router.get("/companies/{id}")
def get_company(id: int):
    return {"one"}

@router.post("/companies")
def add_company():
    return {"added"}

@router.put("/companies/{id}")
def update_company(id: int):
    return {"updated"}

@router.delete("/companies/{id}")
def delete_company(id: int):
    return {"deleted"}