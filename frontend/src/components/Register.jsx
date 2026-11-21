
import { useState } from "react";

export default function Register({ onLogin }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleRegister() {
        try {
            const res = await fetch("http://127.0.0.1:8001/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            const data = await res.json();

            if (!res.ok) {
                setMessage(data.detail || "Registration failed");
                return;
            }

            setMessage(data.message || "Registration successful!");

        } catch (error) {
            setMessage("Cannot connect to server");
        }
    }

    return (
        <>
            <h2>Register</h2>

            <input
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />

            <br /><br />

            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />

            <br /><br />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />

            <br /><br />

            <button onClick={handleRegister}>
                Register
            </button>

            <p>{message}</p>

            <button onClick={onLogin}>
                Back to Login
            </button>
        </>
    );
}
