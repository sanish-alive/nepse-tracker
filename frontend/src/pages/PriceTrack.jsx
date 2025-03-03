import PriceTrackAlert from "../components/PriceTrackAlert";
import { useState, useEffect } from "react";
import { getPriceTracker, getSecurities, submitPriceTrack } from "../services/api";
import "../styles/PriceTrack.css";
import PriceTrackAlertForm from "../components/PriceTrackAlertFrom";

function PriceTrack() {
    const [isOpen, setIsOpen] = useState(false);
    const [priceTrack, setPriceTrack] = useState([]);
    const [securities, setSecurities] = useState([]);
    const [reload,setReload] = useState(false)
    const [isEdit, setIsEdit] = useState(false)

    useEffect(() => {
        const loadPriceTracker = async () => {
            try {
                const priceAlerts = await getPriceTracker();
                setPriceTrack(priceAlerts);
            } catch (err) {
                console.error(err);
            } finally {
                setReload(false)
            }
        };
        loadPriceTracker()
    }, [reload])

    useEffect(() => {
        if (isOpen || isEdit) {
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
    }, [isOpen, isEdit]);

    return (
        <div className="datatable-container">
            {isOpen && (
                <PriceTrackAlertForm securities={securities} setIsOpen={setIsOpen} />
            )}

            <PriceTrackAlert detail={priceTrack} setIsOpen={setIsOpen} setReload={setReload} setIsEdit={setIsEdit} securities={securities} />
        </div>
    );
}

export default PriceTrack;
