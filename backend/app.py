import streamlit as st
import requests

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Enterprise AI Travel Copilot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f7fb;
    }

    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #6b7280;
        margin-bottom: 25px;
    }

    .user-box {

        background:
            linear-gradient(
                135deg,
                #2563eb,
                #1d4ed8
            );

        color: white;

        padding: 14px;

        border-radius: 18px;

        margin-bottom: 12px;

        margin-left: 50px;

        box-shadow:
            0px 4px 12px
            rgba(0,0,0,0.12);
    }

    .assistant-box {

        background: white;

        color: #111827;

        padding: 14px;

        border-radius: 18px;

        margin-bottom: 12px;

        margin-right: 50px;

        box-shadow:
            0px 4px 12px
            rgba(0,0,0,0.08);
    }

    .trip-summary {

        background:
            linear-gradient(
                135deg,
                #111827,
                #1f2937
            );

        color: white;

        padding: 28px;

        border-radius: 24px;

        margin-bottom: 25px;

        box-shadow:
            0px 8px 24px
            rgba(0,0,0,0.18);
    }

    .trip-price {

        font-size: 42px;

        font-weight: 700;

        color: #34d399;

        margin-top: 12px;
    }

    .timeline-card {

        background: white;

        padding: 22px;

        border-radius: 20px;

        margin-bottom: 18px;

        border-left:
            6px solid #2563eb;

        box-shadow:
            0px 4px 12px
            rgba(0,0,0,0.08);
    }

    .timeline-title {

        font-size: 22px;

        font-weight: 700;

        color: #111827;

        margin-bottom: 8px;
    }

    .timeline-sub {

        color: #6b7280;

        margin-bottom: 6px;
    }

    .timeline-price {

        color: #059669;

        font-size: 24px;

        font-weight: bold;

        margin-top: 10px;
    }

    .chip {

        display: inline-block;

        padding: 8px 14px;

        border-radius: 999px;

        font-size: 13px;

        font-weight: 600;

        margin-right: 10px;

        margin-bottom: 12px;
    }

    .green-chip {

        background: #dcfce7;

        color: #166534;
    }

    .orange-chip {

        background: #fed7aa;

        color: #9a3412;
    }

    .red-chip {

        background: #fee2e2;

        color: #991b1b;
    }

    .cost-card {

        background: white;

        padding: 24px;

        border-radius: 20px;

        box-shadow:
            0px 4px 12px
            rgba(0,0,0,0.08);

        margin-top: 15px;
    }

    .cost-row {

        display: flex;

        justify-content: space-between;

        margin-bottom: 12px;
    }

    .cost-total {

        font-size: 24px;

        font-weight: 700;

        color: #111827;
    }

    .policy-warning {

        background: #fee2e2;

        color: #991b1b;

        padding: 12px;

        border-radius: 12px;

        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# SESSION STATE
# =========================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

if "awaiting_approval" not in st.session_state:

    st.session_state.awaiting_approval = False
# =========================================
# CONVERSATIONAL MEMORY
# =========================================

if "last_trip_prompt" not in st.session_state:

    st.session_state.last_trip_prompt = ""
# =========================================
# BACKEND URL
# =========================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =========================================
# LAYOUT
# =========================================

left_col, right_col = st.columns([1, 1.5])

# =========================================
# LEFT PANEL
# =========================================

with left_col:

    st.markdown(
        """
        <div class='main-title'>
        AI Travel Copilot
        </div>

        <div class='sub-title'>
        Enterprise Business Travel Planner
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================
    # CHAT HISTORY
    # =====================================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f"""
                <div class='user-box'>
                {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class='assistant-box'>
                {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

    employee_id = st.selectbox(
        "Employee",
        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    # =====================================
    # USER INPUT
    # =====================================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        # =================================
        # APPROVAL FLOW
        # =================================

        if st.session_state.awaiting_approval:

            lower_input = user_input.lower()

            # =============================
            # APPROVE
            # =============================

            if lower_input in [

                "yes",
                "y",
                "approve",
                "proceed",
                "go ahead",
                "submit approval"
            ]:

                assistant_reply = """
Approval workflow initiated successfully.

✔ Approval Status: Approved

✔ Manager approval simulated successfully

✔ Booking process can now proceed

✔ Your itinerary has been confirmed
"""

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": assistant_reply
                })

                st.session_state.awaiting_approval = False

                st.rerun()

            # =============================
            # CANCEL
            # =============================

            elif lower_input in [

                "no",
                "cancel",
                "stop"
            ]:

                assistant_reply = """
Understood.

The itinerary was NOT submitted for approval.

No bookings were made.
"""

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": assistant_reply
                })

                st.session_state.awaiting_approval = False

                st.rerun()

        # =================================
        # NORMAL FLOW
        # =================================

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        try:

            with st.spinner(

                "Optimizing itinerary..."
            ):

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.trip_data = data

                itinerary = data.get(

                    "itinerary",

                    {}
                )

                approval = data.get(

                    "approval",

                    {}
                )

                approval_required = approval.get(

                    "approval_required",

                    False
                )

                # =========================
                # APPROVAL REQUIRED
                # =========================

                if approval_required:

                    st.session_state.awaiting_approval = True

                    assistant_reply = f"""
I found an optimized itinerary for your business trip.

However approval is required because:

• {approval.get('reason')}

Would you like me to proceed with manager approval?
"""

                # =========================
                # POLICY COMPLIANT
                # =========================

                else:

                    assistant_reply = f"""
Your itinerary is ready.

✔ Flights selected:
{len(itinerary.get('selected_flights', []))}

✔ Hotels selected:
{len(itinerary.get('selected_hotels', []))}

✔ Estimated total cost:
₹{itinerary.get('total_trip_cost', 0)}

The trip is policy compliant and ready for booking.
"""

                st.session_state.messages.append({

                    "role": "assistant",

                    "content": assistant_reply
                })

                st.rerun()

            else:

                st.error(

                    f"Backend Error: {response.status_code}"
                )

        except Exception as e:

            st.error(str(e))

# =========================================
# RIGHT PANEL
# =========================================

with right_col:

    data = st.session_state.trip_data

    if not data:

        st.info(
            "No itinerary generated yet."
        )

    else:

        itinerary = data.get(
            "itinerary",
            {}
        )

        flights = itinerary.get(
            "selected_flights",
            []
        )

        hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        # =================================
        # ROUTE
        # =================================

        route_parts = []

        for flight in flights:

            route_parts.append(
                flight.get("source", "")
            )

        if flights:

            route_parts.append(
                flights[-1].get(
                    "destination",
                    ""
                )
            )

        trip_route = " → ".join(
            route_parts
        )

        # =================================
        # SUMMARY
        # =================================

        st.markdown(
            f"""
            <div class='trip-summary'>

            <h1>
            Optimized Enterprise Itinerary
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(flights)} Flights
            •
            🏨 {len(hotels)} Hotels
            </p>

            <div class='trip-price'>
            ₹ {total_cost}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================
        # STATUS CHIPS
        # =================================

        status_html = ""

        if policy.get("compliant"):

            status_html += """
            <span class='chip green-chip'>
            Policy Compliant
            </span>
            """

        else:

            status_html += """
            <span class='chip red-chip'>
            Policy Violations
            </span>
            """

        if approval.get(
            "approval_required"
        ):

            status_html += """
            <span class='chip orange-chip'>
            Approval Required
            </span>
            """

        st.markdown(
            status_html,
            unsafe_allow_html=True
        )

        st.markdown(
            "### Trip Timeline"
        )

        # =================================
        # TIMELINE
        # =================================

        for i in range(len(flights)):

            flight = flights[i]

            st.markdown(
                f"""
                <div class='timeline-card'>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                Airline:
                {flight.get('airline')}
                </div>

                <div class='timeline-sub'>
                Flight ID:
                {flight.get('flight_id')}
                </div>

                <div class='timeline-sub'>
                Departure:
                {flight.get('departure_time')}
                </div>

                <div class='timeline-sub'>
                Arrival:
                {flight.get('arrival_time')}
                </div>

                <div class='timeline-sub'>
                Stops:
                {flight.get('stops')}
                </div>

                <div class='timeline-price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if i < len(hotels):

                hotel = hotels[i]

                st.markdown(
                    f"""
                    <div class='timeline-card'>

                    <div class='timeline-title'>
                    🏨 {hotel.get('hotel_name')}
                    </div>

                    <div class='timeline-sub'>
                    City:
                    {hotel.get('city')}
                    </div>

                    <div class='timeline-sub'>
                    Area:
                    {hotel.get('location_area')}
                    </div>

                    <div class='timeline-sub'>
                    Rating:
                    ⭐ {hotel.get('rating')}
                    </div>

                    <div class='timeline-sub'>
                    Hotel ID:
                    {hotel.get('hotel_id')}
                    </div>

                    <div class='timeline-price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # =================================
        # POLICY ANALYSIS
        # =================================

        st.markdown(
            "### Policy Analysis"
        )

        violations = policy.get(
            "violations",
            []
        )

        if not violations:

            st.success(
                "Trip is policy compliant"
            )

        else:

            for violation in violations:

                if isinstance(
                    violation,
                    str
                ):

                    st.markdown(
                        f"""
                        <div class='policy-warning'>
                        {violation}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                elif isinstance(
                    violation,
                    dict
                ):

                    st.markdown(
                        f"""
                        <div class='policy-warning'>
                        {violation.get('description', '')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )