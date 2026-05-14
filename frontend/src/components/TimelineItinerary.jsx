function TimelineItinerary({ data }) {
    if (!data) {
        return (
            <div className="empty-state">
                <h2>No itinerary yet</h2>
                <p>Start with a trip request in the conversation.</p>
            </div>
        );
    }

    const itinerary = data.itinerary || {};
    const flights = itinerary.selected_flights || [];
    const hotels = itinerary.selected_hotels || [];
    const transports = data.transports || itinerary.selected_transports || [];
    const totalCost = itinerary.total_trip_cost || 0;
    const days = data.itinerary_days || [];
    const policy = data.policy || {};
    const approval = data.approval || {};
    const warnings = data.recommendation_warnings || [];
    const route = buildRoute(flights);

    return (
        <div className="timeline-container">
            <div className="trip-summary-card">
                <div>
                    <span className="eyebrow">Optimized itinerary</span>
                    <h2>{route || "Business trip"}</h2>
                    <p>{itinerary.optimization_reason}</p>
                </div>
                <div className="cost-block">
                    <span>Total cost</span>
                    <strong>INR {totalCost}</strong>
                </div>
            </div>

            <div className="summary-grid">
                <SummaryTile label="Flights" value={flights.length} />
                <SummaryTile label="Hotels" value={hotels.length} />
                <SummaryTile label="Transport" value={transports.length} />
                <SummaryTile label="Approval" value={approval.status || "not required"} />
            </div>

            <div className="status-strip">
                <div className={`pill ${policy.compliant ? "success" : "danger"}`}>
                    {policy.compliant ? "Policy compliant" : "Policy violations"}
                </div>
                <div className={`pill ${approval.approval_required ? "warning" : "success"}`}>
                    {approval.approval_required ? "Approval required" : "No approval needed"}
                </div>
            </div>

            {warnings.length > 0 && (
                <div className="warning-card">
                    <strong>Limited mock data</strong>
                    <p>
                        Some recommendations could not be generated because the mock
                        database does not contain every route or city.
                    </p>
                    {warnings.map((warning, index) => (
                        <div key={index}>{warning}</div>
                    ))}
                </div>
            )}

            <div className="section-card">
                <div className="section-header">
                    <span>Timeline</span>
                    <strong>Day-wise planner</strong>
                </div>

                {days.length === 0 && (
                    <div className="no-results">
                        No day-wise itinerary could be generated. Try a supported
                        mock route such as Chennai to Bangalore, Hyderabad, and Mumbai.
                    </div>
                )}

                {days.map((day) => (
                    <div className="day-card" key={`${day.day}-${day.city}`}>
                        <div className="day-header">
                            <span>Day {day.day}</span>
                            <strong>{day.city}</strong>
                            <small>{day.date}</small>
                        </div>

                        <div className="timeline-list">
                            {day.timeline?.map((item, index) => (
                                <div className="timeline-item" key={`${item.type}-${index}`}>
                                    <div className={`timeline-dot ${item.type}`} />
                                    <div className="timeline-content">
                                        <span>{item.time}</span>
                                        <strong>{item.title}</strong>
                                        <p>{item.details}</p>
                                        {item.cost ? <small>INR {item.cost}</small> : null}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <SelectedOptions
                flights={flights}
                hotels={hotels}
                transports={transports}
            />
        </div>
    );
}

function SummaryTile({ label, value }) {
    return (
        <div className="summary-tile">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
    );
}

function SelectedOptions({ flights, hotels, transports }) {
    return (
        <div className="section-card">
            <div className="section-header">
                <span>Selected options</span>
                <strong>Flights, hotels, and local travel</strong>
            </div>

            <div className="option-grid">
                {flights.map((flight) => (
                    <div className="option-card" key={flight.flight_id}>
                        <span>Flight</span>
                        <strong>{flight.airline} · {flight.flight_id}</strong>
                        <p>{flight.source} to {flight.destination}</p>
                        <small>{flight.departure_time} to {flight.arrival_time} · INR {flight.price}</small>
                    </div>
                ))}

                {hotels.map((hotel) => (
                    <div className="option-card" key={hotel.hotel_id}>
                        <span>Hotel</span>
                        <strong>{hotel.hotel_name}</strong>
                        <p>{hotel.city} · {hotel.location_area}</p>
                        <small>Rating {hotel.rating} · INR {hotel.price_per_night}/night</small>
                    </div>
                ))}

                {transports.map((transport) => (
                    <div className="option-card" key={transport.transport_id}>
                        <span>Transport</span>
                        <strong>{transport.transport_type}</strong>
                        <p>{transport.city} · {transport.coverage_area}</p>
                        <small>{transport.comfort_level} comfort · INR {transport.estimated_cost}</small>
                    </div>
                ))}
            </div>
        </div>
    );
}

function buildRoute(flights) {
    if (!flights.length) return "";

    const route = [flights[0].source];
    flights.forEach((flight) => {
        if (flight.destination) route.push(flight.destination);
    });

    return route.filter(Boolean).join(" -> ");
}

export default TimelineItinerary;
