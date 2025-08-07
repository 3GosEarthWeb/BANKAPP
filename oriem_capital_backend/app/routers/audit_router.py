from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_audit_logs():
    return {"message": "Audit logs fetched"}
