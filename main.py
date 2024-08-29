from fastapi import FastAPI

app = FastAPI()


@app.get("/companies")
def get_companies():
    return {"all"}

@app.get("/companies/{id}")
def get_company(id: int):
    return {"one"}

@app.post("/companies")
def add_company():
    return {"added"}

@app.put("/companies/{id}")
def update_company(id: int):
    return {"updated"}

@app.delete("/companies/{id}")
def delete_company(id: int):
    return {"deleted"}

@app.get("/companies/{company_id}/employees")
def get_employees(company_id: int):
    return {"all"}

@app.post("/companies/{company_id}/employees")
def add_employee(company_id: int):
    return {"added"}

@app.get("/employees/{id}")
def get_employee(id: int):
    return {"one"}


@app.put("/employees/{id}")
def update_employee(id: int):
    return {"updated"}

@app.delete("/employees/{id}")
def delete_employee(id: int):
    return {"deleted"}

@app.get("/assets")
def get_assets():
    return{"all"}

@app.get("/assets/{id}")
def get_asset(id: int):
    return {"one"}

@app.post("/assets")
def add_asset():
    return {"added"}

@app.put("/assets/{id}")
def update_asset(id: int):
    return {"updated"}

@app.delete("/assets/{id}")
def delete_asset(id: int):
    return {"deleted"}

@app.post("assets/{id}/assign")
def asset_assign(id: int):
    return {"assinged"}

@app.post("/assets/{id}/unassign")
def asset_unassing(id: int):
    return {"unassinged"}