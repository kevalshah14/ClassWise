import React from 'react';
import './WelcomePage.css'; // Import the CSS animation

const WelcomePage = () => {
    return (
        <div className="flex flex-col items-center justify-center h-screen text-white animated-bg px-4">
            <div className="text-center max-w-3xl p-8 space-y-6">
                <h1 className="text-4xl md:text-6xl font-extrabold">
                    Welcome to ClassWise!
                </h1>
                <p className="text-lg md:text-xl leading-relaxed">
                    Stay ahead with instant notifications when a seat opens for your class.
                </p>
                <p className="text-lg md:text-xl leading-relaxed">
                    Never miss an opportunity to secure your spot.
                </p>
                <button className="px-6 py-3 bg-white text-blue-500 font-medium text-lg rounded-lg hover:bg-gray-200 transition transform hover:scale-110 hover:shadow-lg active:scale-95">
                    Get Started
                </button>
            </div>
        </div>
    );
};

export default WelcomePage;
