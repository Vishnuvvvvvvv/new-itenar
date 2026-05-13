from pydantic import BaseModel


class FrontendTripRequest(
    BaseModel
):

    user_input: str

    employee_id: str