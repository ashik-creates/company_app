from fastapi import APIRouter

router = APIRouter(
    tags= ["employee_api"]

)



@router.get("/companies/{company_id}/employees")
def get_employees(company_id: int):
    return {"all"}

@router.post("/companies/{company_id}/employees")
def add_employee(company_id: int):
    return {"added"}

@router.get("/employees/{id}")
def get_employee(id: int):
    return {"one"}


@router.put("/employees/{id}")
def update_employee(id: int):
    return {"updated"}

@router.delete("/employees/{id}")
def delete_employee(id: int):
    return {"deleted"}