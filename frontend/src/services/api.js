const API_BASE = "http://127.0.0.1:8000";

export async function planTrip(payload) {

    const response = await fetch(
        `${API_BASE}/frontend-plan-trip`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        }
    );

    if (!response.ok) {
        throw new Error("Backend request failed");
    }

    return response.json();
}