import { createContext, useContext, useState, useEffect } from "react";
import { authCheck, logout } from "../services/api";

// Create Context
const AuthContext = createContext();

// Auth Provider Component
export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Check authentication on component mount
    useEffect(() => {
        const checkAuth = async () => {
            try {
                const auth = await authCheck();
                setIsAuthenticated(auth); // Ensure it's a boolean
            } catch (error) {
                console.error("Auth check failed:", error);
                setIsAuthenticated(false);
            }
        };
        checkAuth();
    }, [])

    // Login function to update state
    const login = async () => {
        setIsAuthenticated(true);
    };

    // Logout function
    const handleLogout = async () => {
        try {
            await logout();
            setIsAuthenticated(false); // Ensure logout updates UI
        } catch (error) {
            console.error("Logout failed:", error);
        }
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, login, handleLogout }}>
            {children}
        </AuthContext.Provider>
    );
};

// Custom Hook to use AuthContext
export const useAuth = () => useContext(AuthContext);
