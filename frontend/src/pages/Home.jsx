import {useState, useEffect} from "react"
import {getOnline} from "../services/api"

function Home() {
    const [online, setOnline] = useState([])
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const onlineStatus = async () => {
            try {
                const online = await getOnline()
                setOnline(online)
            } catch (err) {
                console.log(err)
                setError("Failed to load.")
            } finally {
                setLoading(false)
            }
        }
        onlineStatus()
    }, [])

    return (
        <div className="home">
            {loading ? (
                <p>loading</p>
            ) : (
                <p>{online.message}</p>
            )}
        </div>
    )
}

export default Home