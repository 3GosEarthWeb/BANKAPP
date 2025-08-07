from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_transactions():
    return {"message": "List of transactions"}

@router.post("/transfer")
def transfer_funds():
    return {"message": "Funds transferred"}
