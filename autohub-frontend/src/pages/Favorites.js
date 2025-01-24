import React, { useEffect, useState } from "react";
import { getFavorites } from '../services/api';

function Favorites (){
    const [favorites, setFavorites] = useState({});

    useEffect(() => {
        async function fetchFavorites() {
            try {
                const response = await getFavorites();
                setFavorites(response.data);
            } catch (error) {
                console.error('Error fetching favorites:', error);
            }
        };
        fetchFavorites();
    }, [])

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