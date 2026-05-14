import { useState } from "react";

function ChatPanel({
    messages,
    onSend,
    loading
}) {

    const [input, setInput] = useState("");

    const handleSubmit = () => {

        if (!input.trim()) return;

        onSend(input);

        setInput("");
    };

    return (
        <div className="chat-container">

            <div className="chat-header">
                <div>
                    <span>Copilot conversation</span>
                    <strong>Plan, revise, approve, and book</strong>
                </div>
            </div>

            <div className="chat-messages">

                {messages.map((msg, index) => (

                    <div
                        key={index}
                        className={`message ${msg.role}`}
                    >
                        <pre>{formatMessage(msg.text, msg.role)}</pre>
                    </div>
                ))}

                {loading && (
                    <div className="message assistant">
                        Planning itinerary...
                    </div>
                )}

            </div>

            <div className="chat-input-area">

                <textarea
                    placeholder="Describe a trip or ask for a change, e.g. avoid Hyderabad..."
                    value={input}
                    onChange={(e) =>
                        setInput(e.target.value)
                    }
                    onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            handleSubmit();
                        }
                    }}
                />

                <button onClick={handleSubmit}>
                    Send
                </button>

            </div>

        </div>
    );
}

function formatMessage(text, role) {
    if (role !== "assistant") return text;

    if (!text) return "";

    if (
        text.includes("SELECTED FLIGHTS") ||
        text.includes("DAY-WISE ITINERARY")
    ) {
        const approvalLine = text.includes("Approval is required")
            ? "\n\nApproval is required. Reply yes, proceed, or approve to continue."
            : "\n\nThe full itinerary is shown in the workspace on the right.";

        return `I generated the optimized itinerary.${approvalLine}\n\nWould you like to make any changes?`;
    }

    return text;
}

export default ChatPanel;
