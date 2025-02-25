import { Link } from "react-router-dom";
import "../styles/Navbar.css"
import { useAuth } from "../context/AuthContext";

function NavBar() {
    const { isAuthenticated, handleLogout } = useAuth()

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">Nepse Tracker</Link>
            </div>
            <div className="navbar-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/price-track" className="nav-link">Price Track</Link>
                <Link to="/open-ipo" className="nav-link"> Open IPO</Link>
                {isAuthenticated ? (
                    <>
                        <Link to="/profile" className="nav-link"> 😎</Link>
                        <Link to="/" className="nav-link" onClick={handleLogout}> Logout</Link>
                    </>
                ) : (
                    <Link to="/login" className="nav-link"> Login</Link>
                )}


            </div>
        </nav>
    )
}

export default NavBar