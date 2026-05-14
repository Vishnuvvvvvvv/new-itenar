from fastapi import APIRouter, HTTPException

from app.models.frontend_request import (
    ApprovalRequest,
    BookingRequest,
    ChatRequest,
)
from app.services.session_service import (
    session_service,
)


router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        return session_service.chat(
            request.session_id,
            request.message,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/approve-trip")
def approve_trip(request: ApprovalRequest):
    try:
        return session_service.apply_approval_decision(
            request.session_id,
            request.decision,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/finalize-booking")
def finalize_booking(request: BookingRequest):
    try:
        return session_service.finalize_booking(
            request.session_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )
