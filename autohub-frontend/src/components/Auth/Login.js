import React, { useState } from "react";
import { login } from "../../services/api";

function Login({ onLoginSuccess }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleSubmit() {
        e.preventDefault();
        try {
            const response = await login({ username, password });
            localStorage.setItem("accessToken", response.dat.access);
            localStorage.setItem("refreshToken", response.data.refresh);
            onLoginSuccess();
        } catch (error) {
            console.error("Login failed", error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Username:
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </label>
            <br />
            <label>
                Password:
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </label>
            <br />
            <button type="submit">Login</button>
        </form>
    );
};

export default login