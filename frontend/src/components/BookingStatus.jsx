function BookingStatus({ data }) {
    const status = data?.status || "not_started";
    const references = data?.references || [];

    return (
        <div className="booking-card">
            <span>Booking state</span>
            <strong>{status.replace("_", " ")}</strong>
            {references.map((item) => (
                <div className="booking-ref" key={item.reference}>
                    <small>{item.type}</small>
                    <span>{item.reference}</span>
                </div>
            ))}
        </div>
    );
}

export default BookingStatus;
