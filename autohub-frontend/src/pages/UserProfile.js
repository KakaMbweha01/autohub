import React, { useEffect, useState } from "react";
import { getProfile } from "../services/api";
import Loader from "../components/Loader";
import Message from "../components/Message";

const Profile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        getProfile()
            .then((response) => {
                setProfile(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError("Failed to load profile.");
                setLoading(false);
            });
    }, []);

    if (loading) return <Loader />;
    if (error) return <Message variant="danger">{error}</Message>;

    return (
        <div>
            <h1>User Profile</h1>
            {profile && (
                <div>
                    <p><strong>Name:</strong> {profile.name}</p>
                    <p><strong>Email:</strong> {profile.email}</p>
                </div>
            )}
        </div>
    );
}

export default Profile;