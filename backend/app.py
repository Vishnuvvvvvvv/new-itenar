import streamlit as st
import requests
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Enterprise AI Travel Copilot",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""

<style>

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;

    background-color: #f4f7fb;
}

/* =========================
   HEADER
========================= */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: #111827;

    margin-bottom: 5px;
}

.sub-title {

    color: #6b7280;

    margin-bottom: 25px;
}

/* =========================
   CHAT
========================= */

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-left: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.assistant-message {

    background: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-right: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* =========================
   TRIP HEADER
========================= */

.trip-header {

    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 22px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

.trip-cost {

    font-size: 38px;

    font-weight: bold;

    color: #34d399;
}

/* =========================
   TIMELINE
========================= */

.timeline-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 18px;

    border-left: 6px solid #2563eb;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.timeline-date {

    font-size: 18px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 12px;
}

.timeline-title {

    font-size: 22px;

    font-weight: bold;

    color: #111827;

    margin-bottom: 10px;
}

.timeline-sub {

    color: #6b7280;

    margin-bottom: 8px;
}

.price {

    font-size: 22px;

    font-weight: bold;

    color: #059669;
}

/* =========================
   STATUS CHIPS
========================= */

.chip {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;

    font-size: 13px;

    font-weight: 600;
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

/* =========================
   COST SUMMARY
========================= */

.summary-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    margin-bottom: 18px;
}

.summary-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 14px;
}

.summary-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 10px;
}

/* =========================
   POLICY
========================= */

.policy-warning {

    background: #fee2e2;

    color: #991b1b;

    padding: 12px;

    border-radius: 12px;

    margin-top: 10px;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

# =====================================
# API
# =====================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([1, 1.6])

# =====================================
# LEFT PANEL
# =====================================

with left_col:

    st.markdown(

        """
        <div class='main-title'>
        Enterprise AI Travel Copilot
        </div>

        <div class='sub-title'>
        Intelligent business trip orchestration
        </div>
        """,

        unsafe_allow_html=True
    )

    # =========================
    # CHAT HISTORY
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(

                f"""
                <div class='user-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.markdown(

                f"""
                <div class='assistant-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    employee_id = st.selectbox(

        "Employee",

        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    # =========================
    # SEND
    # =========================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        with st.spinner(
            "Optimizing itinerary..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

                if response.status_code != 200:

                    st.error(
                        "Backend error occurred"
                    )

                else:

                    data = response.json()

                    st.session_state.trip_data = data

                    itinerary = data.get(
                        "itinerary",
                        {}
                    )

                    selected_flights = itinerary.get(
                        "selected_flights",
                        []
                    )

                    selected_hotels = itinerary.get(
                        "selected_hotels",
                        []
                    )

                    assistant_message = f"""
I found the best itinerary for your business trip.

✔ {len(selected_flights)} optimized flights selected

✔ {len(selected_hotels)} business hotels selected

✔ Total estimated cost: ₹{itinerary.get('total_trip_cost', 0)}

The itinerary has been optimized based on:
• timing preferences
• policy compliance
• office proximity
• business convenience
"""

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": assistant_message
                    })

                    st.rerun()

            except Exception as e:

                st.error(str(e))

# =====================================
# RIGHT PANEL
# =====================================

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

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        transports = data.get(
            "transports",
            []
        )

        calendar_analysis = data.get(
            "calendar_analysis",
            {}
        )

        selected_flights = itinerary.get(
            "selected_flights",
            []
        )

        selected_hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        # =====================================
        # HEADER
        # =====================================

        trip_route = " → ".join([

            flight.get("source", "")

            for flight in selected_flights
        ])

        if selected_flights:

            trip_route += (
                " → "
                + selected_flights[-1].get(
                    "destination",
                    ""
                )
            )

        st.markdown(

            f"""
            <div class='trip-header'>

            <h1>
            Enterprise Business Trip
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(selected_flights)} Flights
            •
            🏨 {len(selected_hotels)} Hotels
            </p>

            <div class='trip-cost'>
            ₹ {total_cost}
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # STATUS
        # =====================================

        compliant = policy.get(
            "compliant",
            False
        )

        status_html = ""

        if compliant:

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

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # =====================================
        # TIMELINE
        # =====================================

        st.subheader(
            "Trip Timeline"
        )

        for index in range(
            len(selected_flights)
        ):

            flight = selected_flights[index]

            hotel = None

            if index < len(selected_hotels):

                hotel = selected_hotels[index]

            st.markdown(

                f"""
                <div class='timeline-card'>

                <div class='timeline-date'>
                Flight {index + 1}
                </div>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                {flight.get('airline')}
                •
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

                <div class='price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,

                unsafe_allow_html=True
            )

            if hotel:

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

                    <div class='price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # COST SUMMARY
        # =====================================

        flight_cost = sum([

            f.get("price", 0)

            for f in selected_flights
        ])

        hotel_cost = sum([

            h.get("price_per_night", 0)

            for h in selected_hotels
        ])

        transport_cost = sum([

            t.get(
                "estimated_cost",
                0
            )

            for t in transports
        ])

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-title'>
            Cost Breakdown
            </div>

            <div class='summary-row'>
            <span>Flights</span>
            <span>₹ {flight_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Hotels</span>
            <span>₹ {hotel_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Transport</span>
            <span>₹ {transport_cost}</span>
            </div>

            <hr>

            <div class='summary-row'>
            <strong>Total</strong>
            <strong>₹ {total_cost}</strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # POLICY WARNINGS
        # =====================================

        violations = policy.get(
            "violations",
            []
        )

        if violations:

            st.subheader(
                "Policy Analysis"
            )

            for violation in violations:

                st.markdown(

                    f"""
                    <div class='policy-warning'>
                    {violation.get('description')}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # APPROVAL
        # =====================================

        st.subheader(
            "Approval Workflow"
        )

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-row'>
            <span>Approval Required</span>
            <strong>
            {approval.get('approval_required')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Approval Level</span>
            <strong>
            {approval.get('approval_level')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Reason</span>
            <strong>
            {approval.get('reason')}
            </strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )import streamlit as st
import requests
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Enterprise AI Travel Copilot",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""

<style>

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;

    background-color: #f4f7fb;
}

/* =========================
   HEADER
========================= */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: #111827;

    margin-bottom: 5px;
}

.sub-title {

    color: #6b7280;

    margin-bottom: 25px;
}

/* =========================
   CHAT
========================= */

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-left: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.assistant-message {

    background: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-right: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* =========================
   TRIP HEADER
========================= */

.trip-header {

    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 22px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

.trip-cost {

    font-size: 38px;

    font-weight: bold;

    color: #34d399;
}

/* =========================
   TIMELINE
========================= */

.timeline-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 18px;

    border-left: 6px solid #2563eb;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.timeline-date {

    font-size: 18px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 12px;
}

.timeline-title {

    font-size: 22px;

    font-weight: bold;

    color: #111827;

    margin-bottom: 10px;
}

.timeline-sub {

    color: #6b7280;

    margin-bottom: 8px;
}

.price {

    font-size: 22px;

    font-weight: bold;

    color: #059669;
}

/* =========================
   STATUS CHIPS
========================= */

.chip {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;

    font-size: 13px;

    font-weight: 600;
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

/* =========================
   COST SUMMARY
========================= */

.summary-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    margin-bottom: 18px;
}

.summary-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 14px;
}

.summary-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 10px;
}

/* =========================
   POLICY
========================= */

.policy-warning {

    background: #fee2e2;

    color: #991b1b;

    padding: 12px;

    border-radius: 12px;

    margin-top: 10px;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

# =====================================
# API
# =====================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([1, 1.6])

# =====================================
# LEFT PANEL
# =====================================

with left_col:

    st.markdown(

        """
        <div class='main-title'>
        Enterprise AI Travel Copilot
        </div>

        <div class='sub-title'>
        Intelligent business trip orchestration
        </div>
        """,

        unsafe_allow_html=True
    )

    # =========================
    # CHAT HISTORY
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(

                f"""
                <div class='user-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.markdown(

                f"""
                <div class='assistant-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    employee_id = st.selectbox(

        "Employee",

        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    # =========================
    # SEND
    # =========================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        with st.spinner(
            "Optimizing itinerary..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

                if response.status_code != 200:

                    st.error(
                        "Backend error occurred"
                    )

                else:

                    data = response.json()

                    st.session_state.trip_data = data

                    itinerary = data.get(
                        "itinerary",
                        {}
                    )

                    selected_flights = itinerary.get(
                        "selected_flights",
                        []
                    )

                    selected_hotels = itinerary.get(
                        "selected_hotels",
                        []
                    )

                    assistant_message = f"""
I found the best itinerary for your business trip.

✔ {len(selected_flights)} optimized flights selected

✔ {len(selected_hotels)} business hotels selected

✔ Total estimated cost: ₹{itinerary.get('total_trip_cost', 0)}

The itinerary has been optimized based on:
• timing preferences
• policy compliance
• office proximity
• business convenience
"""

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": assistant_message
                    })

                    st.rerun()

            except Exception as e:

                st.error(str(e))

# =====================================
# RIGHT PANEL
# =====================================

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

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        transports = data.get(
            "transports",
            []
        )

        calendar_analysis = data.get(
            "calendar_analysis",
            {}
        )

        selected_flights = itinerary.get(
            "selected_flights",
            []
        )

        selected_hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        # =====================================
        # HEADER
        # =====================================

        trip_route = " → ".join([

            flight.get("source", "")

            for flight in selected_flights
        ])

        if selected_flights:

            trip_route += (
                " → "
                + selected_flights[-1].get(
                    "destination",
                    ""
                )
            )

        st.markdown(

            f"""
            <div class='trip-header'>

            <h1>
            Enterprise Business Trip
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(selected_flights)} Flights
            •
            🏨 {len(selected_hotels)} Hotels
            </p>

            <div class='trip-cost'>
            ₹ {total_cost}
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # STATUS
        # =====================================

        compliant = policy.get(
            "compliant",
            False
        )

        status_html = ""

        if compliant:

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

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # =====================================
        # TIMELINE
        # =====================================

        st.subheader(
            "Trip Timeline"
        )

        for index in range(
            len(selected_flights)
        ):

            flight = selected_flights[index]

            hotel = None

            if index < len(selected_hotels):

                hotel = selected_hotels[index]

            st.markdown(

                f"""
                <div class='timeline-card'>

                <div class='timeline-date'>
                Flight {index + 1}
                </div>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                {flight.get('airline')}
                •
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

                <div class='price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,

                unsafe_allow_html=True
            )

            if hotel:

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

                    <div class='price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # COST SUMMARY
        # =====================================

        flight_cost = sum([

            f.get("price", 0)

            for f in selected_flights
        ])

        hotel_cost = sum([

            h.get("price_per_night", 0)

            for h in selected_hotels
        ])

        transport_cost = sum([

            t.get(
                "estimated_cost",
                0
            )

            for t in transports
        ])

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-title'>
            Cost Breakdown
            </div>

            <div class='summary-row'>
            <span>Flights</span>
            <span>₹ {flight_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Hotels</span>
            <span>₹ {hotel_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Transport</span>
            <span>₹ {transport_cost}</span>
            </div>

            <hr>

            <div class='summary-row'>
            <strong>Total</strong>
            <strong>₹ {total_cost}</strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # POLICY WARNINGS
        # =====================================

        violations = policy.get(
            "violations",
            []
        )

        if violations:

            st.subheader(
                "Policy Analysis"
            )

            for violation in violations:

                st.markdown(

                    f"""
                    <div class='policy-warning'>
                    {violation.get('description')}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # APPROVAL
        # =====================================

        st.subheader(
            "Approval Workflow"
        )

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-row'>
            <span>Approval Required</span>
            <strong>
            {approval.get('approval_required')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Approval Level</span>
            <strong>
            {approval.get('approval_level')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Reason</span>
            <strong>
            {approval.get('reason')}
            </strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )import streamlit as st
import requests
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Enterprise AI Travel Copilot",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""

<style>

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;

    background-color: #f4f7fb;
}

/* =========================
   HEADER
========================= */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: #111827;

    margin-bottom: 5px;
}

.sub-title {

    color: #6b7280;

    margin-bottom: 25px;
}

/* =========================
   CHAT
========================= */

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-left: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.assistant-message {

    background: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-right: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* =========================
   TRIP HEADER
========================= */

.trip-header {

    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 22px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

.trip-cost {

    font-size: 38px;

    font-weight: bold;

    color: #34d399;
}

/* =========================
   TIMELINE
========================= */

.timeline-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 18px;

    border-left: 6px solid #2563eb;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.timeline-date {

    font-size: 18px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 12px;
}

.timeline-title {

    font-size: 22px;

    font-weight: bold;

    color: #111827;

    margin-bottom: 10px;
}

.timeline-sub {

    color: #6b7280;

    margin-bottom: 8px;
}

.price {

    font-size: 22px;

    font-weight: bold;

    color: #059669;
}

/* =========================
   STATUS CHIPS
========================= */

.chip {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;

    font-size: 13px;

    font-weight: 600;
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

/* =========================
   COST SUMMARY
========================= */

.summary-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    margin-bottom: 18px;
}

.summary-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 14px;
}

.summary-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 10px;
}

/* =========================
   POLICY
========================= */

.policy-warning {

    background: #fee2e2;

    color: #991b1b;

    padding: 12px;

    border-radius: 12px;

    margin-top: 10px;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

# =====================================
# API
# =====================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([1, 1.6])

# =====================================
# LEFT PANEL
# =====================================

with left_col:

    st.markdown(

        """
        <div class='main-title'>
        Enterprise AI Travel Copilot
        </div>

        <div class='sub-title'>
        Intelligent business trip orchestration
        </div>
        """,

        unsafe_allow_html=True
    )

    # =========================
    # CHAT HISTORY
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(

                f"""
                <div class='user-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.markdown(

                f"""
                <div class='assistant-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    employee_id = st.selectbox(

        "Employee",

        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    # =========================
    # SEND
    # =========================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        with st.spinner(
            "Optimizing itinerary..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

                if response.status_code != 200:

                    st.error(
                        "Backend error occurred"
                    )

                else:

                    data = response.json()

                    st.session_state.trip_data = data

                    itinerary = data.get(
                        "itinerary",
                        {}
                    )

                    selected_flights = itinerary.get(
                        "selected_flights",
                        []
                    )

                    selected_hotels = itinerary.get(
                        "selected_hotels",
                        []
                    )

                    assistant_message = f"""
I found the best itinerary for your business trip.

✔ {len(selected_flights)} optimized flights selected

✔ {len(selected_hotels)} business hotels selected

✔ Total estimated cost: ₹{itinerary.get('total_trip_cost', 0)}

The itinerary has been optimized based on:
• timing preferences
• policy compliance
• office proximity
• business convenience
"""

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": assistant_message
                    })

                    st.rerun()

            except Exception as e:

                st.error(str(e))

# =====================================
# RIGHT PANEL
# =====================================

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

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        transports = data.get(
            "transports",
            []
        )

        calendar_analysis = data.get(
            "calendar_analysis",
            {}
        )

        selected_flights = itinerary.get(
            "selected_flights",
            []
        )

        selected_hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        # =====================================
        # HEADER
        # =====================================

        trip_route = " → ".join([

            flight.get("source", "")

            for flight in selected_flights
        ])

        if selected_flights:

            trip_route += (
                " → "
                + selected_flights[-1].get(
                    "destination",
                    ""
                )
            )

        st.markdown(

            f"""
            <div class='trip-header'>

            <h1>
            Enterprise Business Trip
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(selected_flights)} Flights
            •
            🏨 {len(selected_hotels)} Hotels
            </p>

            <div class='trip-cost'>
            ₹ {total_cost}
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # STATUS
        # =====================================

        compliant = policy.get(
            "compliant",
            False
        )

        status_html = ""

        if compliant:

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

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # =====================================
        # TIMELINE
        # =====================================

        st.subheader(
            "Trip Timeline"
        )

        for index in range(
            len(selected_flights)
        ):

            flight = selected_flights[index]

            hotel = None

            if index < len(selected_hotels):

                hotel = selected_hotels[index]

            st.markdown(

                f"""
                <div class='timeline-card'>

                <div class='timeline-date'>
                Flight {index + 1}
                </div>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                {flight.get('airline')}
                •
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

                <div class='price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,

                unsafe_allow_html=True
            )

            if hotel:

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

                    <div class='price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # COST SUMMARY
        # =====================================

        flight_cost = sum([

            f.get("price", 0)

            for f in selected_flights
        ])

        hotel_cost = sum([

            h.get("price_per_night", 0)

            for h in selected_hotels
        ])

        transport_cost = sum([

            t.get(
                "estimated_cost",
                0
            )

            for t in transports
        ])

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-title'>
            Cost Breakdown
            </div>

            <div class='summary-row'>
            <span>Flights</span>
            <span>₹ {flight_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Hotels</span>
            <span>₹ {hotel_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Transport</span>
            <span>₹ {transport_cost}</span>
            </div>

            <hr>

            <div class='summary-row'>
            <strong>Total</strong>
            <strong>₹ {total_cost}</strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # POLICY WARNINGS
        # =====================================

        violations = policy.get(
            "violations",
            []
        )

        if violations:

            st.subheader(
                "Policy Analysis"
            )

            for violation in violations:

                st.markdown(

                    f"""
                    <div class='policy-warning'>
                    {violation.get('description')}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # APPROVAL
        # =====================================

        st.subheader(
            "Approval Workflow"
        )

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-row'>
            <span>Approval Required</span>
            <strong>
            {approval.get('approval_required')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Approval Level</span>
            <strong>
            {approval.get('approval_level')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Reason</span>
            <strong>
            {approval.get('reason')}
            </strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )import streamlit as st
import requests
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Enterprise AI Travel Copilot",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""

<style>

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;

    background-color: #f4f7fb;
}

/* =========================
   HEADER
========================= */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: #111827;

    margin-bottom: 5px;
}

.sub-title {

    color: #6b7280;

    margin-bottom: 25px;
}

/* =========================
   CHAT
========================= */

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-left: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.assistant-message {

    background: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-right: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* =========================
   TRIP HEADER
========================= */

.trip-header {

    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 22px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

.trip-cost {

    font-size: 38px;

    font-weight: bold;

    color: #34d399;
}

/* =========================
   TIMELINE
========================= */

.timeline-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 18px;

    border-left: 6px solid #2563eb;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.timeline-date {

    font-size: 18px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 12px;
}

.timeline-title {

    font-size: 22px;

    font-weight: bold;

    color: #111827;

    margin-bottom: 10px;
}

.timeline-sub {

    color: #6b7280;

    margin-bottom: 8px;
}

.price {

    font-size: 22px;

    font-weight: bold;

    color: #059669;
}

/* =========================
   STATUS CHIPS
========================= */

.chip {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;

    font-size: 13px;

    font-weight: 600;
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

/* =========================
   COST SUMMARY
========================= */

.summary-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    margin-bottom: 18px;
}

.summary-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 14px;
}

.summary-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 10px;
}

/* =========================
   POLICY
========================= */

.policy-warning {

    background: #fee2e2;

    color: #991b1b;

    padding: 12px;

    border-radius: 12px;

    margin-top: 10px;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

# =====================================
# API
# =====================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([1, 1.6])

# =====================================
# LEFT PANEL
# =====================================

with left_col:

    st.markdown(

        """
        <div class='main-title'>
        Enterprise AI Travel Copilot
        </div>

        <div class='sub-title'>
        Intelligent business trip orchestration
        </div>
        """,

        unsafe_allow_html=True
    )

    # =========================
    # CHAT HISTORY
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(

                f"""
                <div class='user-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.markdown(

                f"""
                <div class='assistant-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    employee_id = st.selectbox(

        "Employee",

        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    # =========================
    # SEND
    # =========================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        with st.spinner(
            "Optimizing itinerary..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

                if response.status_code != 200:

                    st.error(
                        "Backend error occurred"
                    )

                else:

                    data = response.json()

                    st.session_state.trip_data = data

                    itinerary = data.get(
                        "itinerary",
                        {}
                    )

                    selected_flights = itinerary.get(
                        "selected_flights",
                        []
                    )

                    selected_hotels = itinerary.get(
                        "selected_hotels",
                        []
                    )

                    assistant_message = f"""
I found the best itinerary for your business trip.

✔ {len(selected_flights)} optimized flights selected

✔ {len(selected_hotels)} business hotels selected

✔ Total estimated cost: ₹{itinerary.get('total_trip_cost', 0)}

The itinerary has been optimized based on:
• timing preferences
• policy compliance
• office proximity
• business convenience
"""

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": assistant_message
                    })

                    st.rerun()

            except Exception as e:

                st.error(str(e))

# =====================================
# RIGHT PANEL
# =====================================

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

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        transports = data.get(
            "transports",
            []
        )

        calendar_analysis = data.get(
            "calendar_analysis",
            {}
        )

        selected_flights = itinerary.get(
            "selected_flights",
            []
        )

        selected_hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        # =====================================
        # HEADER
        # =====================================

        trip_route = " → ".join([

            flight.get("source", "")

            for flight in selected_flights
        ])

        if selected_flights:

            trip_route += (
                " → "
                + selected_flights[-1].get(
                    "destination",
                    ""
                )
            )

        st.markdown(

            f"""
            <div class='trip-header'>

            <h1>
            Enterprise Business Trip
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(selected_flights)} Flights
            •
            🏨 {len(selected_hotels)} Hotels
            </p>

            <div class='trip-cost'>
            ₹ {total_cost}
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # STATUS
        # =====================================

        compliant = policy.get(
            "compliant",
            False
        )

        status_html = ""

        if compliant:

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

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # =====================================
        # TIMELINE
        # =====================================

        st.subheader(
            "Trip Timeline"
        )

        for index in range(
            len(selected_flights)
        ):

            flight = selected_flights[index]

            hotel = None

            if index < len(selected_hotels):

                hotel = selected_hotels[index]

            st.markdown(

                f"""
                <div class='timeline-card'>

                <div class='timeline-date'>
                Flight {index + 1}
                </div>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                {flight.get('airline')}
                •
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

                <div class='price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,

                unsafe_allow_html=True
            )

            if hotel:

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

                    <div class='price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # COST SUMMARY
        # =====================================

        flight_cost = sum([

            f.get("price", 0)

            for f in selected_flights
        ])

        hotel_cost = sum([

            h.get("price_per_night", 0)

            for h in selected_hotels
        ])

        transport_cost = sum([

            t.get(
                "estimated_cost",
                0
            )

            for t in transports
        ])

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-title'>
            Cost Breakdown
            </div>

            <div class='summary-row'>
            <span>Flights</span>
            <span>₹ {flight_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Hotels</span>
            <span>₹ {hotel_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Transport</span>
            <span>₹ {transport_cost}</span>
            </div>

            <hr>

            <div class='summary-row'>
            <strong>Total</strong>
            <strong>₹ {total_cost}</strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # POLICY WARNINGS
        # =====================================

        violations = policy.get(
            "violations",
            []
        )

        if violations:

            st.subheader(
                "Policy Analysis"
            )

            for violation in violations:

                st.markdown(

                    f"""
                    <div class='policy-warning'>
                    {violation.get('description')}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # APPROVAL
        # =====================================

        st.subheader(
            "Approval Workflow"
        )

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-row'>
            <span>Approval Required</span>
            <strong>
            {approval.get('approval_required')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Approval Level</span>
            <strong>
            {approval.get('approval_level')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Reason</span>
            <strong>
            {approval.get('reason')}
            </strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )import streamlit as st
import requests
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(

    page_title="Enterprise AI Travel Copilot",

    layout="wide",

    initial_sidebar_state="collapsed"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""

<style>

html, body, [class*="css"]  {

    font-family: 'Segoe UI', sans-serif;

    background-color: #f4f7fb;
}

/* =========================
   HEADER
========================= */

.main-title {

    font-size: 34px;

    font-weight: 700;

    color: #111827;

    margin-bottom: 5px;
}

.sub-title {

    color: #6b7280;

    margin-bottom: 25px;
}

/* =========================
   CHAT
========================= */

.user-message {

    background: linear-gradient(
        135deg,
        #2563eb,
        #1d4ed8
    );

    color: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-left: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.12);
}

.assistant-message {

    background: white;

    padding: 14px;

    border-radius: 16px;

    margin-bottom: 12px;

    margin-right: 40px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* =========================
   TRIP HEADER
========================= */

.trip-header {

    background: linear-gradient(
        135deg,
        #111827,
        #1f2937
    );

    color: white;

    padding: 28px;

    border-radius: 22px;

    margin-bottom: 22px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.18);
}

.trip-cost {

    font-size: 38px;

    font-weight: bold;

    color: #34d399;
}

/* =========================
   TIMELINE
========================= */

.timeline-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    margin-bottom: 18px;

    border-left: 6px solid #2563eb;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.timeline-date {

    font-size: 18px;

    font-weight: bold;

    color: #2563eb;

    margin-bottom: 12px;
}

.timeline-title {

    font-size: 22px;

    font-weight: bold;

    color: #111827;

    margin-bottom: 10px;
}

.timeline-sub {

    color: #6b7280;

    margin-bottom: 8px;
}

.price {

    font-size: 22px;

    font-weight: bold;

    color: #059669;
}

/* =========================
   STATUS CHIPS
========================= */

.chip {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 999px;

    margin-right: 8px;

    font-size: 13px;

    font-weight: 600;
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

/* =========================
   COST SUMMARY
========================= */

.summary-card {

    background: white;

    padding: 22px;

    border-radius: 20px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);

    margin-bottom: 18px;
}

.summary-title {

    font-size: 20px;

    font-weight: bold;

    margin-bottom: 14px;
}

.summary-row {

    display: flex;

    justify-content: space-between;

    margin-bottom: 10px;
}

/* =========================
   POLICY
========================= */

.policy-warning {

    background: #fee2e2;

    color: #991b1b;

    padding: 12px;

    border-radius: 12px;

    margin-top: 10px;
}

</style>

""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "trip_data" not in st.session_state:

    st.session_state.trip_data = None

# =====================================
# API
# =====================================

BACKEND_URL = (
    "http://127.0.0.1:8000/frontend-plan-trip"
)

# =====================================
# LAYOUT
# =====================================

left_col, right_col = st.columns([1, 1.6])

# =====================================
# LEFT PANEL
# =====================================

with left_col:

    st.markdown(

        """
        <div class='main-title'>
        Enterprise AI Travel Copilot
        </div>

        <div class='sub-title'>
        Intelligent business trip orchestration
        </div>
        """,

        unsafe_allow_html=True
    )

    # =========================
    # CHAT HISTORY
    # =========================

    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(

                f"""
                <div class='user-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

        else:

            st.markdown(

                f"""
                <div class='assistant-message'>
                {msg['content']}
                </div>
                """,

                unsafe_allow_html=True
            )

    # =========================
    # USER INPUT
    # =========================

    user_input = st.chat_input(
        "Describe your business trip..."
    )

    employee_id = st.selectbox(

        "Employee",

        [
            "EMP001",
            "EMP002",
            "EMP003"
        ]
    )

    # =========================
    # SEND
    # =========================

    if user_input:

        st.session_state.messages.append({

            "role": "user",

            "content": user_input
        })

        payload = {

            "user_input": user_input,

            "employee_id": employee_id
        }

        with st.spinner(
            "Optimizing itinerary..."
        ):

            try:

                response = requests.post(

                    BACKEND_URL,

                    json=payload
                )

                if response.status_code != 200:

                    st.error(
                        "Backend error occurred"
                    )

                else:

                    data = response.json()

                    st.session_state.trip_data = data

                    itinerary = data.get(
                        "itinerary",
                        {}
                    )

                    selected_flights = itinerary.get(
                        "selected_flights",
                        []
                    )

                    selected_hotels = itinerary.get(
                        "selected_hotels",
                        []
                    )

                    assistant_message = f"""
I found the best itinerary for your business trip.

✔ {len(selected_flights)} optimized flights selected

✔ {len(selected_hotels)} business hotels selected

✔ Total estimated cost: ₹{itinerary.get('total_trip_cost', 0)}

The itinerary has been optimized based on:
• timing preferences
• policy compliance
• office proximity
• business convenience
"""

                    st.session_state.messages.append({

                        "role": "assistant",

                        "content": assistant_message
                    })

                    st.rerun()

            except Exception as e:

                st.error(str(e))

# =====================================
# RIGHT PANEL
# =====================================

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

        policy = data.get(
            "policy",
            {}
        )

        approval = data.get(
            "approval",
            {}
        )

        transports = data.get(
            "transports",
            []
        )

        calendar_analysis = data.get(
            "calendar_analysis",
            {}
        )

        selected_flights = itinerary.get(
            "selected_flights",
            []
        )

        selected_hotels = itinerary.get(
            "selected_hotels",
            []
        )

        total_cost = itinerary.get(
            "total_trip_cost",
            0
        )

        # =====================================
        # HEADER
        # =====================================

        trip_route = " → ".join([

            flight.get("source", "")

            for flight in selected_flights
        ])

        if selected_flights:

            trip_route += (
                " → "
                + selected_flights[-1].get(
                    "destination",
                    ""
                )
            )

        st.markdown(

            f"""
            <div class='trip-header'>

            <h1>
            Enterprise Business Trip
            </h1>

            <p>
            📍 {trip_route}
            </p>

            <p>
            ✈ {len(selected_flights)} Flights
            •
            🏨 {len(selected_hotels)} Hotels
            </p>

            <div class='trip-cost'>
            ₹ {total_cost}
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # STATUS
        # =====================================

        compliant = policy.get(
            "compliant",
            False
        )

        status_html = ""

        if compliant:

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

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # =====================================
        # TIMELINE
        # =====================================

        st.subheader(
            "Trip Timeline"
        )

        for index in range(
            len(selected_flights)
        ):

            flight = selected_flights[index]

            hotel = None

            if index < len(selected_hotels):

                hotel = selected_hotels[index]

            st.markdown(

                f"""
                <div class='timeline-card'>

                <div class='timeline-date'>
                Flight {index + 1}
                </div>

                <div class='timeline-title'>
                ✈ {flight.get('source')}
                →
                {flight.get('destination')}
                </div>

                <div class='timeline-sub'>
                {flight.get('airline')}
                •
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

                <div class='price'>
                ₹ {flight.get('price')}
                </div>

                </div>
                """,

                unsafe_allow_html=True
            )

            if hotel:

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

                    <div class='price'>
                    ₹ {hotel.get('price_per_night')}
                    / night
                    </div>

                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # COST SUMMARY
        # =====================================

        flight_cost = sum([

            f.get("price", 0)

            for f in selected_flights
        ])

        hotel_cost = sum([

            h.get("price_per_night", 0)

            for h in selected_hotels
        ])

        transport_cost = sum([

            t.get(
                "estimated_cost",
                0
            )

            for t in transports
        ])

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-title'>
            Cost Breakdown
            </div>

            <div class='summary-row'>
            <span>Flights</span>
            <span>₹ {flight_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Hotels</span>
            <span>₹ {hotel_cost}</span>
            </div>

            <div class='summary-row'>
            <span>Transport</span>
            <span>₹ {transport_cost}</span>
            </div>

            <hr>

            <div class='summary-row'>
            <strong>Total</strong>
            <strong>₹ {total_cost}</strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )

        # =====================================
        # POLICY WARNINGS
        # =====================================

        violations = policy.get(
            "violations",
            []
        )

        if violations:

            st.subheader(
                "Policy Analysis"
            )

            for violation in violations:

                st.markdown(

                    f"""
                    <div class='policy-warning'>
                    {violation.get('description')}
                    </div>
                    """,

                    unsafe_allow_html=True
                )

        # =====================================
        # APPROVAL
        # =====================================

        st.subheader(
            "Approval Workflow"
        )

        st.markdown(

            f"""
            <div class='summary-card'>

            <div class='summary-row'>
            <span>Approval Required</span>
            <strong>
            {approval.get('approval_required')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Approval Level</span>
            <strong>
            {approval.get('approval_level')}
            </strong>
            </div>

            <div class='summary-row'>
            <span>Reason</span>
            <strong>
            {approval.get('reason')}
            </strong>
            </div>

            </div>
            """,

            unsafe_allow_html=True
        )