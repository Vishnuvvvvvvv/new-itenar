function RankingPanel({ rankings, compact = false }) {
    if (!rankings) return null;

    return (
        <div className={`ranking-panel ${compact ? "compact" : ""}`}>
            <div className="section-header">
                <span>Ranking agent</span>
                <strong>Ranked recommendations</strong>
            </div>
            <RankingGroup title="Flights" items={rankings.flights} nameKey="airline" compact={compact} />
            <RankingGroup title="Hotels" items={rankings.hotels} nameKey="hotel_name" compact={compact} />
            <RankingGroup title="Transport" items={rankings.transports} nameKey="transport_type" compact={compact} />
        </div>
    );
}

function RankingGroup({ title, items = [], nameKey, compact }) {
    if (!items.length) return null;

    const visibleItems = compact ? items.slice(0, 2) : items.slice(0, 4);

    return (
        <div className="ranking-group">
            <div className="ranking-title">{title}</div>
            {visibleItems.map((item, index) => (
                <div className="ranking-row" key={`${title}-${index}`}>
                    <div>
                        <strong>{index === 0 ? "Top pick: " : ""}{item[nameKey]}</strong>
                        {!compact && <small>{describeOption(item)}</small>}
                        <p>{item.ranking_reason}</p>
                    </div>
                    <span>{item.ranking_score}</span>
                </div>
            ))}
        </div>
    );
}

function describeOption(item) {
    if (item.flight_id) {
        return `${item.source} to ${item.destination} · ${item.departure_time} · INR ${item.price}`;
    }
    if (item.hotel_id) {
        return `${item.city} · ${item.location_area} · INR ${item.price_per_night}/night`;
    }
    if (item.transport_id) {
        return `${item.city} · ${item.coverage_area} · INR ${item.estimated_cost}`;
    }
    return "";
}

export default RankingPanel;
