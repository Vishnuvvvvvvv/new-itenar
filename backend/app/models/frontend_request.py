from pydantic import BaseModel


class FrontendTripRequest(
    BaseModel
):

    user_input: str

    employee_id: str


class LoginRequest(BaseModel):

    employee_id: str

    password: str


class ChatRequest(BaseModel):

    session_id: str

    message: str


class ApprovalRequest(BaseModel):

    session_id: str

    decision: str


class BookingRequest(BaseModel):

    session_id: str
