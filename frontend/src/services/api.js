const API_BASE = "http://127.0.0.1:8000";

async function request(path, payload) {
    const response = await fetch(
        `${API_BASE}${path}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        }
    );

    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Backend request failed");
    }

    return response.json();
}

export async function login(payload) {
    return request("/login", payload);
}

export async function sendChat(payload) {
    return request("/chat", payload);
}

export async function approveTrip(payload) {
    return request("/approve-trip", payload);
}

export async function finalizeBooking(payload) {
    return request("/finalize-booking", payload);
}

export async function planTrip(payload) {
    return request("/frontend-plan-trip", payload);
}
