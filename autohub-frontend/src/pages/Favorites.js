import React, { useEffect, useState } from "react";
import { getFavorites } from '../services/api';
import Loader from "../components/Loader";
import Message from "../components/Message";

const Favorites = () => {
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        getFavorites()
            .then((response) => {
                setFavorites(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError("Failed to load favorites.");
                setLoading(false);
            });
    }, []);

    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h1>Your Favorites</h1>
            <ul>
                {favorites.map((car) => (
                    <li key={car.id}>{car.name}</li>
                ))}
            </ul>
        </div>
    )
}

export default Favorites;