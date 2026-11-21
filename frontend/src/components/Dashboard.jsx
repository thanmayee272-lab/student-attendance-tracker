
import { useState, useEffect } from "react";

export default function Dashboard({ logout }) {
    const [records, setRecords] = useState([]);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(true);

    async function loadAttendance() {
        try {
            const token = localStorage.getItem("access_token");

            const res = await fetch("http://127.0.0.1:8001/attendance", {
                method: "GET",
                headers: {
                    "token": token
                }
            });

            if (res.status === 401) {
                logout();
                return;
            }

            const data = await res.json();

            if (!res.ok) {
                setMessage(data.detail || "Could not load attendance");
            } else {
                setRecords(data);
                setMessage("");
            }

        } catch (error) {
            setMessage("Cannot connect to the server");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadAttendance();
    }, []);

    return (
        <>
            <h2>Attendance Dashboard</h2>

            <button onClick={logout}>
                Logout
            </button>

            <h3>My Attendance Records</h3>

            <p>{message}</p>

            {loading && <p>Loading...</p>}

            {!loading && !message && records.length === 0 && (
                <p>No attendance records found.</p>
            )}

            {!loading && records.length > 0 && (
                <table border="1" cellPadding="8">
                    <thead>
                        <tr>
                            <th>Student Name</th>
                            <th>Roll No</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>

                    <tbody>
                        {records.map((record) => (
                            <tr key={record.id}>
                                <td>{record.student_name}</td>
                                <td>{record.roll_no}</td>
                                <td>{record.attendance_date}</td>
                                <td>{record.status}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </>
    );
}
