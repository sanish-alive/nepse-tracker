const BASE_URL = "http://localhost:8000"

export const getOnline = async () => {
    const response = await fetch(`${BASE_URL}/online`)
    const data = await response.json()
    return data
}

export const getRoot = async () => {
    const response = await fetch(`${BASE_URL}`)
    const data = await response.json()
    return data
}

export const login = async (credentails) => {
    const response = await fetch(`${BASE_URL}/signin`, {
        method:"POST",
        credentials:"include",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(credentails)
    })
    return response
}

export const logout = async () => {
    const response = await fetch(`${BASE_URL}/logout`, {
        method: "POST",
        credentials: "include",
    })
    return response
}

export const authCheck = async () => {
    const response = await fetch(`${BASE_URL}/auth/check`, {
        credentials: "include",
    })

    if (!response.ok) return false;
    
    const data = await response.json()
    
    return data.authenticated
}

export const getPriceTracker = async () => {
    const response = await fetch(`${BASE_URL}/price-tracker`, {
        credentials: "include",
    })
    const data = await response.json()
    return data
}

export const submitPriceTrack = async (formData) => {
    const response = await fetch(`${BASE_URL}/price-tracker`, {
        credentials: "include",
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            security_id: parseInt(formData.security_id, 10),  // Ensure integer
            min_target_price: parseFloat(formData.min_target_price), // Ensure float
            max_target_price: parseFloat(formData.max_target_price), // Ensure float
            status: Boolean(formData.status)  // Ensure boolean
        }),
    })

    if (!response.ok) {
        throw new Error("Failed to submit data")
    }
    return await response.json()
}

export const getProfile = async () => {
    const response = await fetch(`${BASE_URL}/profile`, {
        credentials: "include",
    })
    const data = await response.json()
    return data
}

export const getSecurities = async () => {
    const response = await fetch(`${BASE_URL}/securities`, {
        credentials: "include"
    })
    const data = await response.json()
    return data
}