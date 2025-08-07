from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_loans():
    return {"message": "List of loans"}

@router.post("/apply")
def apply_for_loan():
    return {"message": "Loan application submitted"}
