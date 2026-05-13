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
                AI Travel Copilot
            </div>

            <div className="chat-messages">

                {messages.map((msg, index) => (

                    <div
                        key={index}
                        className={`message ${msg.role}`}
                    >
                        {msg.text}
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
                    placeholder="Describe your business trip..."
                    value={input}
                    onChange={(e) =>
                        setInput(e.target.value)
                    }
                />

                <button onClick={handleSubmit}>
                    Send
                </button>

            </div>

        </div>
    );
}

export default ChatPanel;