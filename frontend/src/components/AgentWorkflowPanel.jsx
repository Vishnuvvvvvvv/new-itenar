function AgentWorkflowPanel({ logs = [] }) {
    if (!logs.length) return null;

    return (
        <div className="agent-workflow-panel">
            <div className="section-header">
                <span>LangGraph orchestration</span>
                <strong>Agent workflow</strong>
            </div>

            <div className="agent-step-list">
                {logs.map((log, index) => {
                    const [agent, ...details] = String(log).split(":");
                    return (
                        <div className="agent-step" key={`${log}-${index}`}>
                            <div className="agent-step-index">{index + 1}</div>
                            <div>
                                <strong>{agent}</strong>
                                <p>{details.join(":").trim() || log}</p>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

export default AgentWorkflowPanel;
