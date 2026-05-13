function CalendarPanel({ data }) {

    if (!data) return null;

    return (
        <div className="panel-box">

            <h3>Schedule Analysis</h3>

            {
                data.schedule_analysis?.map(
                    (item, index) => (
                        <div
                            key={index}
                            className="schedule-item"
                        >
                            <div>
                                {item.city}
                            </div>

                            <div>
                                Buffer:
                                {
                                    item.buffer_minutes
                                } mins
                            </div>

                            <div>
                                Risk:
                                {item.risk_level}
                            </div>
                        </div>
                    )
                )
            }

        </div>
    );
}

export default CalendarPanel;