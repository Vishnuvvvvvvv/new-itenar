import requests
import streamlit as st


BACKEND_URL = "http://127.0.0.1:8000"

TRAVEL_KEYWORDS = {
    "travel",
    "trip",
    "flight",
    "flights",
    "hotel",
    "hotels",
    "cab",
    "taxi",
    "metro",
    "transport",
    "meeting",
    "meetings",
    "itinerary",
    "book",
    "booking",
    "approve",
    "approval",
    "policy",
    "budget",
    "cost",
    "chennai",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "mumbai",
    "delhi",
    "avoid",
    "remove",
    "skip",
    "change",
    "modify",
    "finalize",
    "finalise",
    "proceed",
    "yes",
    "no",
    "cancel",
}

SMALL_TALK = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "thanks",
    "thank you",
}


st.set_page_config(
    page_title="Enterprise Travel Copilot",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    :root {
        --ink: #172033;
        --muted: #667085;
        --line: #d9e2ef;
        --soft-line: #edf2f7;
        --surface: #ffffff;
        --bg: #f4f7fb;
        --blue: #1f6feb;
        --navy: #111827;
        --green: #047857;
        --amber: #b45309;
        --red: #b91c1c;
    }

    .stApp {
        background: var(--bg);
        color: var(--ink);
    }

    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 1.5rem;
        max-width: 1440px;
    }

    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--line);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem;
    }

    div[data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 14px 16px;
        min-height: 96px;
    }

    div[data-testid="stMetric"] label {
        color: var(--muted);
    }

    div[data-testid="stMetricValue"] {
        color: var(--ink);
        font-size: 1.35rem;
    }

    .app-title {
        background: var(--navy);
        color: white;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }

    .app-title h1 {
        margin: 0;
        font-size: 28px;
        letter-spacing: 0;
    }

    .app-title p {
        margin: 6px 0 0;
        color: #cbd5e1;
    }

    .login-wrap {
        max-width: 460px;
        margin: 10vh auto 0;
    }

    .metric-card,
    .panel-card,
    .day-card,
    .login-card,
    .empty-card,
    .sidebar-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
    }

    .login-card {
        padding: 22px;
    }

    .login-card h2,
    .panel-card h3,
    .day-card h3 {
        margin-top: 0;
        margin-bottom: 8px;
    }

    .status-pill {
        display: inline-block;
        padding: 7px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        margin: 0 8px 10px 0;
    }

    .success { background: #dcfce7; color: #166534; }
    .warning { background: #fef3c7; color: #92400e; }
    .danger { background: #fee2e2; color: #991b1b; }
    .info { background: #dbeafe; color: #1e40af; }
    .muted { color: var(--muted); }

    .section-label {
        color: var(--muted);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .timeline-item {
        border-left: 2px solid var(--blue);
        padding: 2px 0 14px 14px;
        margin-left: 6px;
    }

    .timeline-item strong {
        display: block;
        margin: 2px 0 3px;
    }

    .timeline-time {
        color: var(--muted);
        font-size: 12px;
        font-weight: 700;
    }

    .ranking-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        border-top: 1px solid var(--soft-line);
        padding: 10px 0;
    }

    .score {
        background: #edf6ff;
        color: #0f4ca8;
        border-radius: 8px;
        min-width: 44px;
        text-align: center;
        padding: 8px;
        font-weight: 800;
    }

    .chat-note {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #9a3412;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }

    .sidebar-card h3 {
        margin: 0 0 6px;
        font-size: 18px;
    }

    .sidebar-card p {
        margin: 4px 0;
    }

    .booking-ref {
        border-top: 1px solid var(--soft-line);
        padding-top: 8px;
        margin-top: 8px;
        font-size: 13px;
    }

    .route-line {
        color: var(--muted);
        margin-top: 4px;
    }

    .stChatMessage {
        border-radius: 8px;
    }

    button[kind="primary"], .stButton > button {
        border-radius: 8px;
        font-weight: 700;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .app-title h1 {
            font-size: 22px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def post(path, payload):
    response = requests.post(
        f"{BACKEND_URL}{path}",
        json=payload,
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def init_state():
    defaults = {
        "session_id": None,
        "employee": None,
        "messages": [],
        "trip_data": None,
        "login_error": "",
        "chat_error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def is_in_scope(message):
    text = (message or "").strip().lower()
    if not text:
        return False

    if text in SMALL_TALK:
        return True

    return any(keyword in text for keyword in TRAVEL_KEYWORDS)


def guardrail_response(message):
    text = (message or "").strip().lower()
    if text in SMALL_TALK:
        return (
            "Hello. I can help plan enterprise travel, modify itineraries, "
            "check policy, manage approvals, and simulate booking."
        )

    return (
        "I can only help with enterprise travel planning in this demo: flights, "
        "hotels, local transport, meetings, policy checks, approvals, itinerary "
        "changes, and booking simulation. Try asking something like: "
        "'Plan a trip from Chennai to Bangalore and Mumbai, avoid morning flights.'"
    )


def login_view():
    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="app-title">
            <h1>Enterprise Travel Copilot</h1>
            <p>Policy-aware business travel planning with approval simulation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=False):
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("### Sign in")
        st.caption("Use an employee from employees.json. Any non-empty demo password works.")
        employee_id = st.text_input("Employee ID", value="EMP001")
        password = st.text_input("Password", value="demo", type="password")

        if st.button("Sign in", use_container_width=True):
            try:
                result = post(
                    "/login",
                    {
                        "employee_id": employee_id,
                        "password": password,
                    },
                )
                st.session_state.session_id = result["session_id"]
                st.session_state.employee = result["employee"]
                st.session_state.messages = [
                    {
                        "role": "assistant",
                        "content": (
                            f"Welcome {result['employee']['employee_name']}. "
                            "Tell me where you need to travel for business."
                        ),
                    }
                ]
                st.session_state.login_error = ""
                st.rerun()
            except Exception as exc:
                st.session_state.login_error = str(exc)

        if st.session_state.login_error:
            st.error(st.session_state.login_error)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def sidebar_view():
    employee = st.session_state.employee or {}
    trip_data = st.session_state.trip_data or {}
    approval = trip_data.get("approval", {})
    booking = trip_data.get("booking_state", {})

    st.sidebar.markdown(
        """
        <div class="app-title">
            <h1>Travel Copilot</h1>
            <p>Enterprise itinerary desk</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div class="sidebar-card">
            <div class="section-label">Employee</div>
            <h3>{employee.get('employee_name', '-')}</h3>
            <p>{employee.get('designation', '')}</p>
            <p class="muted">{employee.get('department', '')} · {employee.get('employee_location', '')}</p>
            <p class="muted">{employee.get('employee_id', '')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div class="sidebar-card">
            <div class="section-label">Trip Status</div>
            <p>Approval: <strong>{approval.get('status', 'not_started')}</strong></p>
            <p>Booking: <strong>{booking.get('status', 'not_started')}</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if booking.get("references"):
        st.sidebar.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.sidebar.markdown("<div class='section-label'>Booking References</div>", unsafe_allow_html=True)
        for item in booking["references"]:
            st.sidebar.markdown(
                f"<div class='booking-ref'>{item['type']}: <strong>{item['reference']}</strong></div>",
                unsafe_allow_html=True,
            )
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if st.sidebar.button("Logout", use_container_width=True):
        for key in ["session_id", "employee", "messages", "trip_data"]:
            st.session_state[key] = None if key != "messages" else []
        st.rerun()


def chat_view():
    st.markdown(
        """
        <div class="panel-card">
            <div class="section-label">Copilot Conversation</div>
            <h3>Plan, revise, approve, and book</h3>
            <p class="muted">This assistant is scoped to enterprise travel workflows.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chat_box = st.container(height=520)
    with chat_box:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    user_input = st.chat_input(
        "Describe a trip or ask for a change, e.g. avoid Hyderabad"
    )

    if user_input:
        if not is_in_scope(user_input):
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": guardrail_response(user_input),
                }
            )
            st.session_state.chat_error = ""
            st.rerun()

        try:
            result = post(
                "/chat",
                {
                    "session_id": st.session_state.session_id,
                    "message": user_input,
                },
            )
            st.session_state.trip_data = result
            st.session_state.messages = result.get(
                "messages",
                st.session_state.messages,
            )
            st.session_state.chat_error = ""
            st.rerun()
        except Exception as exc:
            st.session_state.chat_error = str(exc)

    if st.session_state.chat_error:
        st.error(st.session_state.chat_error)


def itinerary_view():
    data = st.session_state.trip_data

    if not data:
        st.markdown(
            """
            <div class="empty-card">
                <div class="section-label">Workspace</div>
                <h3>No itinerary yet</h3>
                <p class="muted">Start with a travel request such as Chennai to Bangalore and Mumbai.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    itinerary = data.get("itinerary", {})
    policy = data.get("policy", {})
    approval = data.get("approval", {})
    booking = data.get("booking_state", {})

    route = build_route_label(itinerary.get("selected_flights", []))
    st.markdown(
        f"""
        <div class="panel-card">
            <div class="section-label">Optimized Itinerary</div>
            <h3>{route or 'Business trip'}</h3>
            <div class="route-line">Generated from mock flights, hotels, transport, calendar, and policy data.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cost", f"INR {itinerary.get('total_trip_cost', 0)}")
    col2.metric("Approval", approval.get("status", "not_started"))
    col3.metric("Booking", booking.get("status", "not_started"))

    if policy.get("compliant", True):
        st.markdown(
            "<span class='status-pill success'>Policy compliant</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<span class='status-pill danger'>Policy violations</span>",
            unsafe_allow_html=True,
        )

    if approval.get("approval_required"):
        st.markdown(
            "<span class='status-pill warning'>Approval required</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="chat-note">
                Reply yes, proceed, or approve in chat to simulate manager approval.
            </div>
            """,
            unsafe_allow_html=True,
        )

    can_finalize = (
        not approval.get("approval_required")
        or approval.get("status") == "approved"
    ) and booking.get("status") != "booked"

    if can_finalize:
        if st.button("Finalize booking", use_container_width=True):
            try:
                result = post(
                    "/finalize-booking",
                    {
                        "session_id": st.session_state.session_id,
                    },
                )
                st.session_state.trip_data = result
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result.get(
                            "assistant_message",
                            "Booking finalized.",
                        ),
                    }
                )
                st.rerun()
            except Exception as exc:
                st.error(str(exc))

    st.markdown("### Day-wise itinerary")
    for day in data.get("itinerary_days", []):
        st.markdown(
            f"""
            <div class="day-card">
                <h3>Day {day.get('day')} - {day.get('city')}</h3>
                <p class="muted">{day.get('date')}</p>
            """,
            unsafe_allow_html=True,
        )

        for item in day.get("timeline", []):
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">{item.get('time', '')}</div>
                    <strong>{item.get('title', '')}</strong>
                    <div class="muted">{item.get('details', '')}</div>
                    <div>{'INR ' + str(item.get('cost')) if item.get('cost') else ''}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    ranking_view(data.get("rankings", {}))


def ranking_view(rankings):
    if not rankings:
        return

    st.markdown("### Ranked recommendations")
    render_ranking_group("Flights", rankings.get("flights", []), "airline")
    render_ranking_group("Hotels", rankings.get("hotels", []), "hotel_name")
    render_ranking_group(
        "Transport",
        rankings.get("transports", []),
        "transport_type",
    )


def render_ranking_group(title, items, name_key):
    if not items:
        return

    with st.expander(title, expanded=title == "Flights"):
        for item in items[:5]:
            st.markdown(
                f"""
                <div class="ranking-row">
                    <div>
                        <strong>{item.get(name_key, '-')}</strong>
                        <div class="muted">{item.get('ranking_reason', '')}</div>
                    </div>
                    <div class="score">{item.get('ranking_score', 0)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def build_route_label(flights):
    if not flights:
        return ""

    route_parts = []
    for flight in flights:
        source = flight.get("source")
        if source and source not in route_parts:
            route_parts.append(source)

    destination = flights[-1].get("destination")
    if destination:
        route_parts.append(destination)

    return " -> ".join(route_parts)


def main():
    init_state()

    if not st.session_state.session_id:
        login_view()
        return

    sidebar_view()

    left, right = st.columns([0.95, 1.25], gap="large")
    with left:
        chat_view()
    with right:
        itinerary_view()


if __name__ == "__main__":
    main()
