import React, { useEffect, useState } from "react";
import axios from 'axios';
import { getNotifications } from "../services/api";

/* const Notifications = () => {
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/notifications/', {
            headers: {
                Authorization: `4f7a65231d5d80a5bd5f20a361dd95727cbb8da0`
            }
        }).then(response => {
            setNotifications(response.data);
        }).catch(error => {
            console.error("Error fetching notifications", error);
        });
    }, []); */

    function Notifications(){
        const [notifications, setNotifications] = useState([]);

        useEffect(() => {
            async function fetchData() {
                try {
                    const data = await getNotifications();
                    setNotifications(data);
                } catch (error) {
                    console.error('Failed to fetch notifications:', error);
                }
            }
            fetchData();
        }, []);

        return (
            <div>
                <h2>Notifications</h2>
                <ul>
                    {notifications.map(notif => (
                        <li key={notif.id}>{notif.message}</li>
                    ))}
                </ul>
            </div>
        );
    };
//};

export default Notifications;