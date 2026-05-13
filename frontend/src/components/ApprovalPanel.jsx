function ApprovalPanel({ data }) {

    if (!data) return null;

    return (
        <div className="panel-box">

            <h3>Approval Workflow</h3>

            <div>
                Required:
                {
                    data.approval_required
                        ? " Yes"
                        : " No"
                }
            </div>

            <div>
                Level: {data.approval_level}
            </div>

            <div>
                Reason: {data.reason}
            </div>

        </div>
    );
}

export default ApprovalPanel;