import React, { useEffect, useState } from 'react';
import { getUserProfile, getNotifications} from '../services/api';

function Home() {
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
}

export default Home;