import React from 'react';
import './SignUpPage.css'; // Import custom CSS

const SignUpPage = () => {
    return (
        <div className="animated-bg flex flex-col items-center justify-center h-screen bg-gradient-to-br from-blue-500 to-purple-600 text-white px-4">
            <div className="sign-up-card">
                <h1 className="sign-up-title">Create Your DeQueue Account</h1>
                {/* Sign-Up Form */}
                <form className="space-y-6">
                    <div className="input-group">
                        <label htmlFor="name" className="input-label">
                            Full Name
                        </label>
                        <input
                            type="text"
                            id="name"
                            className="input-field"
                            placeholder="Enter your full name"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="email" className="input-label">
                            Email Address
                        </label>
                        <input
                            type="email"
                            id="email"
                            className="input-field"
                            placeholder="Enter your email"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label htmlFor="password" className="input-label">
                            Password
                        </label>
                        <input
                            type="password"
                            id="password"
                            className="input-field"
                            placeholder="Create a password"
                            required
                        />
                    </div>
                    <button type="submit" className="primary-button">
                        Sign Up
                    </button>
                </form>

                {/* OR Divider */}
                <div className="or-divider">
                    <span className="or-text">OR</span>
                </div>

                {/* Google Sign-Up */}
                <button className="google-button">
                    <img
                        src="https://developers.google.com/identity/images/g-logo.png"
                        alt="Google logo"
                        className="google-logo"
                    />
                    Sign up with Google
                </button>

                {/* Sign-In Link */}
                <p className="sign-in-text">
                    Already have an account?{' '}
                    <a href="/signin" className="sign-in-link">
                        Sign In
                    </a>
                </p>
            </div>
        </div>
    );
};

export default SignUpPage;
