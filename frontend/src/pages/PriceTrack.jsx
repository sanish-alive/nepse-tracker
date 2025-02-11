import PriceTrackAlert from "../components/PriceTrackAlert"
import {useState, useEffect} from "react"
import { getOnline, getPriceTracker, getRoot } from "../services/api"
import "../styles/Home.css"

function PriceTrack() {
    const [searchQuery, setSearchQuery] = useState("")
    // const priceAlerts = [
    //     {id: 1, symbol: "NIFRA", min_price: 111, max_price: 222, created_at: 23123},
    //     {id: 2, symbol: "APFL", min_price: 234, max_price: 645, created_at: 4123},
    //     {id: 3, symbol: "NABIL", min_price: 352, max_price: 822, created_at: 123}
    // ]


    const [priceTrack, setPriceTrack] = useState([])
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadPriceTracker = async () => {
            try {
                const priceAlerts = await getPriceTracker()
                setPriceTrack(priceAlerts)
                console.log(priceAlerts)
            } catch (err) {
                console.log(err)
                setError("Failed to Load...")
            }
            finally {
                setLoading(false)
            }
            
        }
        loadPriceTracker()
    }, [])

    const handleSearch = (e) => {
        e.preventDefault()
        alert(searchQuery)
    }

    // return (
    //     <div className="home">
    //         <form onSubmit={handleSearch} className="search-alert-form">
    //             <input
    //              type="text"
    //              placeholder="Search for alerts..."
    //              className="search-input"
    //              value={searchQuery}
    //              onChange={(e) => setSearchQuery(e.target.value)}
    //             />
    //             <button type="submit" className="search-button">Search</button>
    //         </form>
    //         <div className="alerts-grid">
    //             {priceTrack.map((alert) => (
    //                 alert.symbol.toLowerCase().startsWith(searchQuery) && (
    //                     <PriceTrackAlert detail={alert} key={alert.id} />
    //                 )
    //             ))}
    //         </div>
    //     </div>
    // )
}

export default PriceTrack