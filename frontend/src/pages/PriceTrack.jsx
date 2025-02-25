import PriceTrackAlert from "../components/PriceTrackAlert";
import { useState, useEffect } from "react";
import { getPriceTracker, getSecurities, submitPriceTrack } from "../services/api";
import "../styles/PriceTrack.css";
import PriceTrackAlertForm from "../components/PriceTrackAlertFrom";

function PriceTrack() {
    const [isOpen, setIsOpen] = useState(false);
    const [priceTrack, setPriceTrack] = useState([]);
    const [securities, setSecurities] = useState([]);    

    useEffect(() => {
        const loadPriceTracker = async () => {
            try {
                const priceAlerts = await getPriceTracker();
                setPriceTrack(priceAlerts);
                console.log(priceAlerts);
            } catch (err) {
                console.error(err);
            }
        };
        loadPriceTracker()
    }, [])

    useEffect(() => {
        if (isOpen) {
            const loadSecurities = async () => {
                try {
                    const ourSecurities = await getSecurities();
                    setSecurities(ourSecurities);
                } catch (err) {
                    console.error(err);
                }
            };
            loadSecurities();
        }
    }, [isOpen]);

    return (
        <div className="datatable-container">
            {isOpen && (
                <PriceTrackAlertForm securities={securities} setIsOpen={setIsOpen}/>
            )}

            <PriceTrackAlert detail={priceTrack} setIsOpen={setIsOpen} />
        </div>
    );
}

export default PriceTrack;
