import React, { useState } from "react";
//import axios from "axios";
import { searchCars } from "../services/api";

/*const Search = () => {
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
    };*/

    function Search() {
        const [query, setQuery] = useState('');
        const [results, setResults] = useState([]);

        const handleSearch = async (e) => {
            e.preventDefault();
            try {
                const response = await searchCars(query);
                setResults(response.data);
            } catch (error) {
                console.error('Search failed:', error);
            }
        };

        return (
            <div>
                <h2>Search Cars</h2>
                <form onSubmit={handleSearch}>
                    <input
                        type="text"
                        placeholder="Search for cars..."
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                    />
                    <button onClick={handleSearch}>Search</button>
                </form>
                <ul>
                    {results.map(car => (
                        <li key={car.id}>{car.name}</li>
                    ))}
                </ul>
            </div>
        );
    };
//};

export default Search;