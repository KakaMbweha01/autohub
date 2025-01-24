import React, { useEffect, useState } from 'react';
import { getCars } from '../services/api';
import Loader from "../components/Loader";
import Message from "../components/Message";

/*function Home() {
    const [profile, setProfile] = useState(null);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        //fetch profile for user
        getUserProfile()
            .then((response) => setProfile(response.data))
            .catch((error) => console.error('Error fetching profile:', error));

        //fetch notifications
        getNotifications()
            .then((response) => setNotifications(response.data))
            .catch((error) => console.error('Error fetching notifications:', error));
    }, []);

    return (
        <div>
            <h2>Welcome to Autohub</h2>
            {profile && (
                <div>
                    <h3>User Profile:</h3>
                    <p>Name: {profile.name} </p>
                    <p>Email: {profile.email} </p>
                </div>
            )}
            <div>
                <h3>Notifications</h3>
                <ul>
                    {notifications.map((notification) => (
                        <li key={notification.id}>{notification.message}</li>
                    ))}
                </ul>
            </div>
        </div>
    )
}*/

const Home = () => {
    const [cars, setCars] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        getCars()
            .then((response) => {
                setCars(response.data);
                setLoading(false);
            })
            .catch((err) => {
                setError("Failed to load cars.");
                setLoading(false);
            });
    }, []);

    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h1>Available Cars</h1>
            <ul>
                {cars.map((car) => (
                    <li key={car.id}>{car.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default Home;