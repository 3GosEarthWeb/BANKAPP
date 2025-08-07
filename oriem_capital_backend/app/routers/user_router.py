from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list_users():
    return {"message": "List of users"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"User {user_id} details"}
