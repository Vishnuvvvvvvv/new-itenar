function PolicyPanel({ data }) {

    if (!data) return null;

    return (
        <div className="panel-box">

            <h3>Policy Status</h3>

            <div>
                Compliance:
                {
                    data.compliant
                        ? " Yes"
                        : " No"
                }
            </div>

            {
                data.violations?.map(
                    (v, index) => (
                        <div
                            key={index}
                            className="warning"
                        >
                            {v.description}
                        </div>
                    )
                )
            }

        </div>
    );
}

export default PolicyPanel;