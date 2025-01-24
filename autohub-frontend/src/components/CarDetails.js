import React, { useEffect, useState } from "react";
import { getCarDetails } from '../services/api';

function CarDetail ({ match }) {
    const [car, setCar] = useState(null);
    const carId = match.params.carId;

    useEffect(() => {
        async function fetchCarDetails() {
            try {
                const response = await getCarDetails(carId);
                setCar(response.data);
            } catch (error) {
                console.error('Error fetching car details:', error);
            }
        };
        fetchCarDetails();
    }, [carId]);

    if (!car) return <div>Loading...</div>;

    return (
        <div>
            <h2>{car.name}</h2>
            <p>Model: {car.model}</p>
            <p>Year: {car.year}</p>;
            <p>Price: Ksh{car.price}</p>
            <p>{car.description}</p>
        </div>
    );
};

export default CarDetail;