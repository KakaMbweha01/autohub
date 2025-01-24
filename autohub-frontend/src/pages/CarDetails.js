import React, { useEffect, useState } from "react";
import { getCarDetails } from '../services/api';
import { useParams } from "react-router-dom";
import Loader from "../components/Loader";
import Message from "../components/Message";

const CarDetail = () => {
    const [car, setCar] = useState(null);
    const { carId } = useParams();
    const [loading, setLoading] = useState("");


    useEffect(() => {
        getCarDetails(carId)
            .then((response) => {
                setCar(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError("Failed to load car details");
                setLoading(false);
            })
    }, [carId]);

    if (!car) return <div>Loading...</div>;
    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h2>{car.name}</h2>
            <p><strong>Model:</strong> {car.model}</p>
            <p><strong>Year:</strong> {car.year}</p>;
            <p><strong>Price:</strong> Ksh{car.price}</p>
            <p>{car.description}</p>
        </div>
    );
};

export default CarDetail;