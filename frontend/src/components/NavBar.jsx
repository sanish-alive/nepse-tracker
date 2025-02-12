import { Link } from "react-router-dom";
import "../styles/Navbar.css"

function NavBar() {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">Home</Link>
            </div>
            <div className="navbar-links">
                <Link to="/" className="nav-link">Home</Link>
                <Link to="/price-track" className="nav-link">Price Track</Link>
                <Link to="/open-ipo" className="nav-link"> Open IPO</Link>
                <Link to="/profile" className="nav-link"> 😎</Link>
            </div>
        </nav>
    )
}

export default NavBar