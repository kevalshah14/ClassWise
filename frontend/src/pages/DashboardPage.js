import React, { useState } from 'react';
import './DashboardPage.css';

const DashboardPage = () => {
    const [classNumber, setClassNumber] = useState('');
    const [classes, setClasses] = useState([]);

    const handleAddClass = () => {
        if (classNumber.trim() === '') return;
        const newClass = {
            id: Date.now(),
            name: `Class ${classNumber}`,
            seats: Math.floor(Math.random() * 50), // Simulated seat data
            notify: false,
        };
        setClasses([...classes, newClass]);
        setClassNumber('');
    };

    const toggleNotify = (id) => {
        setClasses((prevClasses) =>
            prevClasses.map((cls) =>
                cls.id === id ? { ...cls, notify: !cls.notify } : cls
            )
        );
    };

    return (
        <div className="dashboard-page">
            <header className="dashboard-header">
                <h1>Welcome to ClassWise</h1>
                <button className="update-profile-button">Update Profile</button>
            </header>

            {/* Input Section */}
            <div className="input-section">
                <input
                    type="text"
                    value={classNumber}
                    onChange={(e) => setClassNumber(e.target.value)}
                    className="input-field"
                    placeholder="Enter Class Number"
                />
                <button onClick={handleAddClass} className="add-button">
                    Add Class
                </button>
            </div>

            {/* Class Cards */}
            {classes.length > 0 && (
                <div className="class-cards-container">
                    {classes.map((cls) => (
                        <div className="class-card" key={cls.id}>
                            <h2>{cls.name}</h2>
                            <p>Seats: {cls.seats}</p>
                            <div
                                className={`notify-indicator ${
                                    cls.notify ? 'notify-on' : 'notify-off'
                                }`}
                                onClick={() => toggleNotify(cls.id)}
                            ></div>
                            <p className="notify-text">
                                Notify: {cls.notify ? 'On' : 'Off'}
                            </p>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default DashboardPage;
