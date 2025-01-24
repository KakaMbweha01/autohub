import React, { useEffect, useState } from 'react';
import { getCars } from '../services/api';

function CarList(){
    const [cars, setCars] = useState([]);

    useEffect(() => {
        async function fetchCars() {
            try {
                const response = await getCars();
                setCars(response.data);
            } catch (error) {
                console.error('Error fetching cars:', error);
            }
        };
        fetchCars();
    }, []);

    return (
        <div>
            <h2>Car List</h2>
            <ul>
                {cars.map((car) => (
                    <li key={car.id}>
                        {car.name} - {car.model} - {car.year}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default CarList;