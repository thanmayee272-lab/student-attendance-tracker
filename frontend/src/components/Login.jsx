
import { useState } from "react";

export default function Login({ onSuccess, onRegister }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleLogin() {
        try {
            const res = await fetch("http://127.0.0.1:8001/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            });

            const data = await res.json();

            if (!res.ok) {
                setMessage(data.detail || "Login failed");
                return;
            }

            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            onSuccess();

        } catch (error) {
            setMessage("Cannot connect to server");
        }
    }

    return (
        <>
            <h2>Login</h2>

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

            <button onClick={handleLogin}>
                Login
            </button>

            <p>{message}</p>

            <button onClick={onRegister}>
                Create Account
            </button>
        </>
    );
}
