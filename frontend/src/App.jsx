import { useState } from "react";

import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";

import "./App.css";

function App() {

    const [page, setPage] = useState(
        localStorage.getItem("access_token") ? "dashboard" : "login"
    );

    function handleLogout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        setPage("login");
    }

    function handleLoginSuccess() {
        setPage("dashboard");
    }

    return (
        <div className="app">

            <h1>Student Attendance Tracker</h1>

            {page === "register" && (
                <Register
                    onLogin={() => setPage("login")}
                />
            )}

            {page === "login" && (
                <Login
                    onSuccess={handleLoginSuccess}
                    onRegister={() => setPage("register")}
                />
            )}

            {page === "dashboard" && (
                <Dashboard
                    logout={handleLogout}
                />
            )}

        </div>
    );
}

export default App;
