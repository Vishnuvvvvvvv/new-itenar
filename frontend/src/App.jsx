import { useMemo, useState } from "react";

import "./App.css";

import ChatPanel from "./components/ChatPanel";
import EmployeeProfile from "./components/EmployeeProfile";
import LoginPage from "./components/LoginPage";
import TimelineItinerary from "./components/TimelineItinerary";
import RankingPanel from "./components/RankingPanel";
import ApprovalCard from "./components/ApprovalCard";
import BookingStatus from "./components/BookingStatus";
import AgentWorkflowPanel from "./components/AgentWorkflowPanel";

import { login, sendChat, finalizeBooking } from "./services/api";

function App() {
    const [session, setSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [tripData, setTripData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const tripStatus = useMemo(() => {
        if (!tripData) return "No active itinerary";
        if (tripData.booking_state?.status === "booked") return "Booked";
        if (tripData.approval?.status === "pending") return "Approval pending";
        if (tripData.approval?.status === "approved") return "Approved";
        return "Planning";
    }, [tripData]);

    const handleLogin = async (credentials) => {
        setLoading(true);
        setError("");

        try {
            const response = await login(credentials);
            setSession(response);
            setMessages([
                {
                    role: "assistant",
                    text: `Welcome ${response.employee.employee_name}. Tell me where you need to travel for business.`
                }
            ]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const sendMessage = async (text) => {
        if (!session) return;

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                text
            }
        ]);
        setLoading(true);
        setError("");

        try {
            const response = await sendChat({
                session_id: session.session_id,
                message: text
            });

            setTripData(response);
            setMessages(response.messages?.map((item) => ({
                role: item.role,
                text: item.content
            })) || []);
        } catch (err) {
            setError(err.message);
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: "I could not complete that request. Please check the backend and try again."
                }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleFinalizeBooking = async () => {
        if (!session) return;

        setLoading(true);
        setError("");

        try {
            const response = await finalizeBooking({
                session_id: session.session_id
            });
            setTripData(response);
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: response.assistant_message
                }
            ]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (!session) {
        return (
            <LoginPage
                onLogin={handleLogin}
                loading={loading}
                error={error}
            />
        );
    }

    return (
        <div className="copilot-shell">
            <aside className="sidebar">
                <div className="brand-block">
                    <div className="brand-mark">AI</div>
                    <div>
                        <h1>Travel Copilot</h1>
                        <p>Enterprise itinerary desk</p>
                    </div>
                </div>

                <EmployeeProfile employee={session.employee} />

                <div className="status-panel">
                    <span>Trip status</span>
                    <strong>{tripStatus}</strong>
                </div>

                <BookingStatus data={tripData?.booking_state} />

                <RankingPanel
                    rankings={tripData?.rankings}
                    compact
                />
            </aside>

            <main className="chat-workspace">
                {error && (
                    <div className="error-banner">
                        {error}
                    </div>
                )}

                <ChatPanel
                    messages={messages}
                    onSend={sendMessage}
                    loading={loading}
                />
            </main>

            <section className="itinerary-workspace">
                <ApprovalCard
                    data={tripData?.approval}
                    onFinalize={handleFinalizeBooking}
                    bookingState={tripData?.booking_state}
                    loading={loading}
                />

                <AgentWorkflowPanel logs={tripData?.execution_logs} />

                <TimelineItinerary data={tripData} />
            </section>
        </div>
    );
}

export default App;
