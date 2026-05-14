from fastapi import APIRouter, HTTPException

from app.models.frontend_request import (
    LoginRequest,
)
from app.services.session_service import (
    session_service,
)


router = APIRouter()


@router.post("/login")
def login(request: LoginRequest):
    try:
        return session_service.login(
            request.employee_id,
            request.password,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )
