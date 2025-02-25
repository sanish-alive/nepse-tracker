import { useState, useEffect } from "react"
import "../styles/Login.css"
import { login } from "../services/api"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"

function Login() {
    const [credentials, setCredentials] = useState({
        email: "",
        password: ""
    })
    const navigate = useNavigate()
    const { login: setAuth } = useAuth()

    const handleChange = (e) => {
        const { name, value } = e.target
        setCredentials({
            ...credentials,
            [name]: value
        })
    }

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await login(credentials)
            const data = await response.json()
            if (response.ok) {
                setAuth()
                navigate("/profile")
            } else {
                console.log("login failed:")
            }
        } catch (err) {
            console.log(err)
        }
    }

    return (
        <div className="login-container">

            <div className="login-form">
            <h1>LOGIN</h1>
                <form onSubmit={handleLogin}>
                    <label htmlFor="email">Email:</label>
                    <input
                        id="email"
                        type="text"
                        name="email"
                        value={credentials.email}
                        onChange={handleChange}
                        required
                    />
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={credentials.password}
                        onChange={handleChange}
                        required
                    />
                    <p>Don't have an account? Create.</p>
                    <button type="submit">Login</button>
                </form>
            </div>
        </div>
    )
}

export default Login