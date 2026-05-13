function FlightCard({ flight }) {

    return (
        <div className="card">

            <div className="card-title">
                {flight.airline}
            </div>

            <div>
                {flight.source} → {flight.destination}
            </div>

            <div>
                Departure: {flight.departure_time}
            </div>

            <div>
                Arrival: {flight.arrival_time}
            </div>

            <div>
                Stops: {flight.stops}
            </div>

            <div className="price">
                ₹ {flight.price}
            </div>

        </div>
    );
}

export default FlightCard;