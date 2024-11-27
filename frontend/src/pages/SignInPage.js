import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import './SignInPage.css'; // Import custom CSS

const SignInPage = () => {
    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-br from-blue-500 to-purple-600 text-white px-4">
            <div className="sign-in-card">
                <h1 className="sign-in-title">Sign In to ClassWise</h1>
                <form className="space-y-6">
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
                            placeholder="Enter your password"
                            required
                        />
                    </div>
                    <button type="submit" className="primary-button">
                        Sign In
                    </button>
                </form>
                <div className="or-divider">
                    <span className="or-text">OR</span>
                </div>
                <button className="google-button">
                    <img
                        src="https://developers.google.com/identity/images/g-logo.png"
                        alt="Google logo"
                        className="google-logo"
                    />
                    Sign in with Google
                </button>
                <p className="sign-up-text">
                    Don’t have an account?{' '}
                    <Link to="/signup" className="sign-up-link">
                        Sign Up
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default SignInPage;
