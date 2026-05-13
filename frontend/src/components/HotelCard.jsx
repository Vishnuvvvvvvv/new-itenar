function HotelCard({ hotel }) {

    return (
        <div className="card">

            <div className="card-title">
                {hotel.hotel_name}
            </div>

            <div>
                {hotel.city}
            </div>

            <div>
                {hotel.location_area}
            </div>

            <div>
                Rating: {hotel.rating}
            </div>

            <div className="price">
                ₹ {hotel.price_per_night}
            </div>

        </div>
    );
}

export default HotelCard;