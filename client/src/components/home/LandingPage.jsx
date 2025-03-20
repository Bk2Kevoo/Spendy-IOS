import { Link } from "react-router";


function LandingPage() {
    return (
        <div className="landing-container">
            <div className="video-money">
                <img src="/images/bugs.gif" alt="Bugs Bunny throwing money" />
            </div>
            <div className="landing-information">
                <p className="landing-text">
                    Welcome To Spendy, let's be financially responsible! In this app, you can track expenses, transactions, budgets, and savings all in one. Welcome and get ready to save millions.
                </p>
                <div className="container">
                <div className="register-box">
                    <Link to="/register">
                        <button id="register-button">Register</button>
                    </Link>
                </div>
                <p className="middle-or">or</p>
                <div className="login-box">
                    <Link to="/login">
                        <button id="login-button">Login</button>
                    </Link>
                </div>
            </div>
            </div>
        </div>
    );
}

export default LandingPage;
