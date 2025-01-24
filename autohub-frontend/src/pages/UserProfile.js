import React, { useEffect, useState } from "react";
import { getUserProfile } from "../services/api";

function UserProfile() {
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await getUserProfile();
                setProfile(response.data);
            } catch (error) {
                console.error('Failed to fetch profile:', error);
            }
        }
        fetchData();
    }, []);

    if (!profile) return <p>Loading profile...</p>;

    return (
        <div>
            <h1>User Profile</h1>
            <p><strong>Name:</strong> {profile.name}</p>
            <p><strong>Email:</strong> {profile.email}</p>
        </div>
    );
}

export default UserProfile;