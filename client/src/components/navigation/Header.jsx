import { NavLink } from "react-router-dom";


function Header() {
    return (
        <header>
            <h1 className="logo-name">
                <span className="logo" role="img"></span>
                Spendy 
            </h1>
            <nav className="home-link">
                <NavLink to="/home" className={({ isActive }) => isActive ? "active home-link" : "home-link"}>Home</NavLink>                
            </nav>
            <nav className="about-link">
                <NavLink to="/" className={({ isActive }) => isActive ? "active about-link" : "about-link"}>About</NavLink>
            </nav>
            <nav className="savings-link">
                <NavLink to="/savings" className={({ isActive }) => isActive ? "active savings-link" : "savings-link"}>Savings</NavLink>
            </nav>
            <nav className="analysis-link">
                <NavLink to="/analysis" className={({ isActive }) => isActive ? "active analysis-link" : "analysis-link"}>Analysis</NavLink>
            </nav>
            <nav className="profile-link">
                <NavLink to="/profile" className={({ isActive }) => isActive ? "active profile-link" : "profile-link"}>Profile</NavLink>
            </nav>

        </header>
    )
}

export default Header;