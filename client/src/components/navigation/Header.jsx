import { NavLink } from "react-router-dom/cjs/react-router-dom.min"



const Header = () => {
    return (
        <header>
            <h1>
                <span className="logo" role="img"></span>
                Spendy 
            </h1>

            <nav>
                <NavLink to="/" className={({ isActive }) => isActive ? "active home-link" : "home-link"}>Home</NavLink>


            </nav>
        </header>
    )
}

export default Header;