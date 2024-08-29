from fastapi import APIRouter

router = APIRouter(
    tags= ["asset_api"]

)



@router.get("/assets")
def get_assets():
    return{"all"}

@router.get("/assets/{id}")
def get_asset(id: int):
    return {"one"}

@router.post("/assets")
def add_asset():
    return {"added"}

@router.put("/assets/{id}")
def update_asset(id: int):
    return {"updated"}

@router.delete("/assets/{id}")
def delete_asset(id: int):
    return {"deleted"}

@router.post("assets/{id}/assign")
def asset_assign(id: int):
    return {"assinged"}

@router.post("/assets/{id}/unassign")
def asset_unassing(id: int):
    return {"unassinged"}