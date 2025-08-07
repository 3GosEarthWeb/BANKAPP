from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import register_user, authenticate_user
from app.dependencies.auth_dependencies import get_current_user
from app.database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    summary="Register a new user",
    response_description="User successfully created"
)
def register_user_route(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Register a new user account.
    """
    try:
        return register_user(db, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Registration failed: {str(e)}"
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    response_description="Access token returned"
)
def login_user_route(
    payload: LoginRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Authenticate user and return access token.
    """
    try:
        token, _ = authenticate_user(db, payload)
        return TokenResponse(access_token=token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    response_description="Authenticated user details"
)
def get_current_user_route(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """
    Retrieve the currently authenticated user's info.
    """
    return current_user
