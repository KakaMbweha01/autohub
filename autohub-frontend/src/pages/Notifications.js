import React, { useEffect, useState } from "react";
//import axios from 'axios';
import { getNotifications } from "../services/api";

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        /*axios.get('http://127.0.0.1:8000/notifications/', {
            headers: {
                Authorization: `4f7a65231d5d80a5bd5f20a361dd95727cbb8da0`
            }*/
        getNotifications()
            .then(response => {
                setNotifications(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError("Error fetching notifications");
                setLoading(false);
        });
    }, []);

    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h1>Notifications</h1>
            {notifications.length ? (
                <ul>
                    {notifications.map(notif => (
                        <li key={notif.id}>{notif.message}</li>
                    ))}
                </ul>
            ) : (
                <Message variant="info">No notifications available</Message>
            )}
        </div>
    );
};


export default Notifications;