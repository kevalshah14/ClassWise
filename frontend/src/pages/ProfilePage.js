import React, { useState } from 'react';
import './ProfilePage.css'; // Import custom CSS

const ProfilePage = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        phone: '',
        email: '',
        semester: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Updated Profile:', formData);
        alert('Profile updated successfully!');
    };

    return (
        <div className="animated-bg flex flex-col items-center justify-center h-screen bg-gradient-to-br from-blue-500 to-purple-600 text-white px-4">
            <div className="profile-card">
                <h1 className="profile-title">Your Profile</h1>
                <form onSubmit={handleSubmit} className="space-y-6">
                    {/* First Name */}
                    <div className="input-group">
                        <label htmlFor="firstName" className="input-label">
                            First Name
                        </label>
                        <input
                            type="text"
                            id="firstName"
                            name="firstName"
                            className="input-field"
                            value={formData.firstName}
                            onChange={handleChange}
                            placeholder="Enter your first name"
                            required
                        />
                    </div>
                    {/* Last Name */}
                    <div className="input-group">
                        <label htmlFor="lastName" className="input-label">
                            Last Name
                        </label>
                        <input
                            type="text"
                            id="lastName"
                            name="lastName"
                            className="input-field"
                            value={formData.lastName}
                            onChange={handleChange}
                            placeholder="Enter your last name"
                            required
                        />
                    </div>
                    {/* Phone Number */}
                    <div className="input-group">
                        <label htmlFor="phone" className="input-label">
                            Phone Number
                        </label>
                        <input
                            type="tel"
                            id="phone"
                            name="phone"
                            className="input-field"
                            value={formData.phone}
                            onChange={handleChange}
                            placeholder="Enter your phone number"
                            required
                        />
                    </div>
                    {/* Email */}
                    <div className="input-group">
                        <label htmlFor="email" className="input-label">
                            Email
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            className="input-field"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="Enter your email"
                            required
                        />
                    </div>
                    {/* Semester */}
                    <div className="input-group">
                        <label htmlFor="semester" className="input-label">
                            Semester
                        </label>
                        <input
                            type="text"
                            id="semester"
                            name="semester"
                            className="input-field"
                            value={formData.semester}
                            onChange={handleChange}
                            placeholder="Enter your semester"
                            required
                        />
                    </div>
                    <button type="submit" className="primary-button">
                        Update Profile
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ProfilePage;
