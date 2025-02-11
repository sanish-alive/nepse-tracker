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

export const getPriceTracker = async () => {
    const response = await fetch(`${BASE_URL}/price-tracker`, {
        credentials: "include",
    })
    const data = await response.json()
    return data
}