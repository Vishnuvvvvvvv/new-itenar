function ApprovalCard({ data, onFinalize, bookingState, loading }) {
    if (!data) return null;

    const canFinalize = (
        (!data.approval_required || data.status === "approved") &&
        bookingState?.status !== "booked"
    );

    return (
        <div className={`approval-card ${data.approval_required ? "needs-approval" : ""}`}>
            <div>
                <span>Approval workflow</span>
                <strong>{data.status || "not_required"}</strong>
                <p>{data.reason}</p>
            </div>

            <div className="approval-actions">
                {data.approval_required && data.status === "pending" && (
                    <small>Reply yes, proceed, or approve in chat to simulate manager approval.</small>
                )}

                {canFinalize && (
                    <button onClick={onFinalize} disabled={loading}>
                        {loading ? "Finalizing..." : "Finalize booking"}
                    </button>
                )}
            </div>
        </div>
    );
}

export default ApprovalCard;
