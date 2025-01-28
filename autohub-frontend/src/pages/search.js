import React, { useState,useEffect } from "react";
//import axios from "axios";
import { searchCars } from "../services/api";
import { useSearchParams } from "react-router-dom";
import Loader from "../components/Loader";
import Message from "../components/Message";

const Search = () => {
    //const [searchParams] = useSearchParams();
    const query = useSearchParams.get("q");
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        searchCars(query)
            .then((response) => {
                setResults(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError("Failed to load search results.");
                setLoading(false);
            });
    }, [query]);

    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h2>Search Results for "{query}"</h2>
            <ul>
                {results.map(car => (
                    <li key={car.id}>{car.name}</li>
                ))}
            </ul>
        </div>
    );
};


export default Search;