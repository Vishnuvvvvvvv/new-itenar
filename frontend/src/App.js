import { useState } from "react";

import "./App.css";

import ChatPanel from "./components/ChatPanel";
import ItineraryPanel from "./components/ItineraryPanel";

import { planTrip } from "./services/api";

function App() {

    const [messages, setMessages] = useState([]);

    const [tripData, setTripData] = useState(null);

    const [loading, setLoading] = useState(false);

    const sendMessage = async (text) => {

        const userMessage = {
            role: "user",
            text
        };

        setMessages((prev) => [
            ...prev,
            userMessage
        ]);

        setLoading(true);

        try {

            const payload = {
                user_input: text,
                employee_id: "EMP001"
            };

            const response = await planTrip(
                payload
            );

            setTripData(response);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: response.chat_summary
                }
            ]);

        } catch (error) {

            console.error(error);

            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    text: "Backend error occurred"
                }
            ]);

        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">

            <div className="left-panel">

                <ChatPanel
                    messages={messages}
                    onSend={sendMessage}
                    loading={loading}
                />

            </div>

            <div className="right-panel">

                <ItineraryPanel
                    data={tripData}
                />

            </div>

        </div>
    );
}

export default App;