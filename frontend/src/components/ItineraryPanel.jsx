import FlightCard from "./FlightCard";
import HotelCard from "./HotelCard";
import PolicyPanel from "./PolicyPanel";
import ApprovalPanel from "./ApprovalPanel";
import CalendarPanel from "./CalendarPanel";

function ItineraryPanel({ data }) {

    if (!data) {

        return (
            <div className="empty-panel">
                No itinerary generated yet.
            </div>
        );
    }

    return (
        <div className="itinerary-container">

            <div className="summary-card">

                <h2>Optimized Itinerary</h2>

                <h3>
                    ₹ {data.itinerary?.total_trip_cost}
                </h3>

                <p>
                    {
                        data.itinerary
                            ?.optimization_reason
                    }
                </p>

            </div>

            <div className="section-title">
                Flights
            </div>

            {
                data.itinerary?.selected_flights?.map(
                    (flight) => (
                        <FlightCard
                            key={flight.flight_id}
                            flight={flight}
                        />
                    )
                )
            }

            <div className="section-title">
                Hotels
            </div>

            {
                data.itinerary?.selected_hotels?.map(
                    (hotel) => (
                        <HotelCard
                            key={hotel.hotel_id}
                            hotel={hotel}
                        />
                    )
                )
            }

            <CalendarPanel
                data={data.calendar_analysis}
            />

            <PolicyPanel
                data={data.policy}
            />

            <ApprovalPanel
                data={data.approval}
            />

        </div>
    );
}

export default ItineraryPanel;