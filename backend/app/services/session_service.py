import copy
import uuid
from typing import Any, Dict, List, Optional

from app.db.mock_employee_db import get_employee
from app.services.travel_service import TravelPlannerService


APPROVAL_YES = {
    "yes",
    "y",
    "approve",
    "approved",
    "proceed",
    "go ahead",
    "submit",
    "submit approval",
}

APPROVAL_NO = {
    "no",
    "n",
    "cancel",
    "stop",
    "do not proceed",
    "don't proceed",
}

BOOKING_INTENTS = {
    "book",
    "book it",
    "finalize",
    "finalise",
    "confirm booking",
    "finalize booking",
    "finalise booking",
}


class SessionService:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.travel_service = TravelPlannerService()

    def login(self, employee_id: str, password: str) -> Dict[str, Any]:
        if not password or not password.strip():
            raise ValueError("Password is required.")

        employee = get_employee(employee_id)
        if not employee:
            raise ValueError("Employee not found.")

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "employee": employee,
            "messages": [],
            "latest_request": {},
            "latest_response": None,
            "approval": {
                "approval_required": False,
                "status": "not_required",
            },
            "booking_state": {
                "status": "not_started",
                "references": [],
            },
        }

        return {
            "session_id": session_id,
            "employee": employee,
        }

    def get_session(self, session_id: str) -> Dict[str, Any]:
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Invalid or expired session.")
        return session

    def chat(self, session_id: str, message: str) -> Dict[str, Any]:
        session = self.get_session(session_id)
        text = (message or "").strip()
        normalized = text.lower()

        session["messages"].append(
            {
                "role": "user",
                "content": text,
            }
        )

        if self._is_cancel_intent(normalized) and self._approval_pending(session):
            response = self.apply_approval_decision(session_id, "cancel")
            return self._append_and_return(session, response)

        if self._is_approval_intent(normalized) and self._approval_pending(session):
            response = self.apply_approval_decision(session_id, "approve")
            return self._append_and_return(session, response)

        if self._is_booking_intent(normalized):
            response = self.finalize_booking(session_id)
            return self._append_and_return(session, response)

        result = self.travel_service.run_trip_planner(
            {
                "user_input": text,
                "employee_id": session["employee"]["employee_id"],
                "session_id": session_id,
                "conversation_history": session["messages"],
                "previous_request": session.get("latest_request", {}),
                "booking_state": session.get("booking_state", {}),
            }
        )

        session["booking_state"] = {
            "status": "not_started",
            "references": [],
        }
        session["latest_request"] = result.get("parsed_request", {})
        session["latest_response"] = self._build_response(result, session)
        session["approval"] = session["latest_response"].get("approval", {})

        return self._append_and_return(session, session["latest_response"])

    def apply_approval_decision(
        self,
        session_id: str,
        decision: str
    ) -> Dict[str, Any]:
        session = self.get_session(session_id)
        latest = copy.deepcopy(session.get("latest_response") or {})
        approval = copy.deepcopy(latest.get("approval") or session.get("approval") or {})
        decision = (decision or "").lower()

        if decision in {"approve", "approved", "yes", "proceed"}:
            approval.update(
                {
                    "approval_required": True,
                    "status": "approved",
                    "approval_completed": True,
                    "message": "Manager approval simulated successfully.",
                }
            )
            assistant_message = (
                "Approval completed. Manager approval has been simulated successfully. "
                "You can now finalize the booking."
            )
        else:
            approval.update(
                {
                    "approval_required": True,
                    "status": "cancelled",
                    "approval_completed": False,
                    "message": "Approval flow cancelled by the user.",
                }
            )
            assistant_message = (
                "Approval flow cancelled. No bookings were made for this itinerary."
            )

        latest["approval"] = approval
        latest["assistant_message"] = assistant_message
        session["approval"] = approval
        session["latest_response"] = latest
        return latest

    def finalize_booking(self, session_id: str) -> Dict[str, Any]:
        session = self.get_session(session_id)
        latest = copy.deepcopy(session.get("latest_response") or {})
        if not latest:
            raise ValueError("No itinerary is available to book.")

        approval = latest.get("approval") or {}
        if approval.get("approval_required") and approval.get("status") != "approved":
            latest["assistant_message"] = (
                "Approval is required before booking. Would you like me to proceed with approval?"
            )
            return latest

        itinerary = latest.get("itinerary") or {}
        references: List[Dict[str, str]] = []

        for item in itinerary.get("selected_flights", []):
            references.append(
                {
                    "type": "flight",
                    "id": item.get("flight_id", ""),
                    "reference": f"BK-FLT-{item.get('flight_id', uuid.uuid4().hex[:6]).upper()}",
                    "status": "booked",
                }
            )

        for item in itinerary.get("selected_hotels", []):
            references.append(
                {
                    "type": "hotel",
                    "id": item.get("hotel_id", ""),
                    "reference": f"BK-HTL-{item.get('hotel_id', uuid.uuid4().hex[:6]).upper()}",
                    "status": "booked",
                }
            )

        for item in latest.get("transports", []):
            references.append(
                {
                    "type": "transport",
                    "id": item.get("transport_id", ""),
                    "reference": f"BK-TRN-{item.get('transport_id', uuid.uuid4().hex[:6]).upper()}",
                    "status": "booked",
                }
            )

        booking_state = {
            "status": "booked",
            "references": references,
            "message": "Flights, hotels, and local transport are booked.",
        }

        latest["booking_state"] = booking_state
        latest["assistant_message"] = (
            "Booking confirmed. Flights, hotels, and local transport have been booked."
        )
        session["booking_state"] = booking_state
        session["latest_response"] = latest
        return latest

    def _append_and_return(
        self,
        session: Dict[str, Any],
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        assistant_message = response.get("assistant_message") or response.get("chat_summary") or ""
        if assistant_message:
            session["messages"].append(
                {
                    "role": "assistant",
                    "content": assistant_message,
                }
            )
        response["messages"] = session["messages"]
        return response

    def _build_response(
        self,
        result: Dict[str, Any],
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        approval = result.get("approval_workflow", {})
        assistant_message = result.get("final_response", "")
        warnings = result.get("recommendation_warnings", [])

        if warnings:
            assistant_message += (
                "\n\nSome recommendations could not be generated from the mock data:\n"
                + "\n".join(f"- {warning}" for warning in warnings)
            )

        if approval.get("approval_required") and approval.get("status") == "pending":
            assistant_message += (
                "\n\nApproval is required due to policy violations. "
                "Would you like me to proceed with approval?"
            )
        else:
            assistant_message += (
                "\n\nWould you like to make any changes to your itinerary?"
            )

        return {
            "session_id": session["session_id"],
            "employee": session["employee"],
            "assistant_message": assistant_message,
            "chat_summary": assistant_message,
            "parsed_request": result.get("parsed_request", {}),
            "itinerary": result.get("optimized_itinerary", {}),
            "itinerary_days": result.get("itinerary_days", []),
            "rankings": result.get("ranking_results", {}),
            "flights": result.get("flight_options", []),
            "hotels": result.get("hotel_options", []),
            "transports": result.get("transport_options", []),
            "policy": result.get("policy_results", {}),
            "approval": approval,
            "booking_state": session.get("booking_state", {}),
            "calendar_analysis": result.get("calendar_analysis", {}),
            "execution_logs": result.get("execution_logs", []),
            "recommendation_warnings": warnings,
        }

    def _approval_pending(self, session: Dict[str, Any]) -> bool:
        approval = session.get("approval") or {}
        return approval.get("approval_required") and approval.get("status") == "pending"

    def _is_approval_intent(self, normalized: str) -> bool:
        return normalized in APPROVAL_YES

    def _is_cancel_intent(self, normalized: str) -> bool:
        return normalized in APPROVAL_NO

    def _is_booking_intent(self, normalized: str) -> bool:
        return normalized in BOOKING_INTENTS


session_service = SessionService()
