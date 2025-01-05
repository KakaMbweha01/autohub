import React, { useState } from "react";
import axios from "axios";

const Search = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);

    const handleSearch = () => {
        axios.get(`http://127.0.0.1:8000/search/?q=${query}`)
            .then(response => {
                setResults(response.data);
            })
            .catch(error => {
                console.error("Error during search:", error);
            });
    };
    return (
        <div>
            <h2>Search Cars</h2>
            <input
                type="text"
                placeholder="Search for cars..."
                value={query}
                onChange={e => setQuery(e.target.value)}
            />
            <button onClick={handleSearch}>Search</button>
            <ul>
                {results.map(car => (
                    <li key={car.id}>{car.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default Search;