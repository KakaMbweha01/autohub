import React, { useEffect, useState } from "react";
import { getFavorites } from '../services/api';

function Favorites (){
    const [favorites, setFavorites] = useState({});

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getFavorites();
                setFavorites(data);
            } catch (error) {
                console.error('Error fetching favorites:', error);
            }
        }
        fetchData();
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