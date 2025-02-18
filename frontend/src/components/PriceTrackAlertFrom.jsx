import { useState, useEffect } from "react";
import { submitPriceTrack } from "../services/api";

function PriceTrackAlertForm({securities}) {
    const [formData, setFormData] = useState({
            security_id: "",
            min_target_price: "",
            max_target_price: "",
            status: true,
        });
    const handleChange = (e) => {
            const { name, value, type, checked } = e.target;
            setFormData({
                ...formData,
                [name]: type === "checkbox" ? checked : value,
            });
        };
    
        const handleSubmit = (e) => {
            e.preventDefault();
            try {
                const response = submitPriceTrack(formData)
                alert("Price alert is added.")
            } catch (err) {
                console.log(err)
            } finally {
                setIsOpen(false);
            }
        };
    return (
        <div className="popup-overlay">
            <div className="popup-content">
                <h2>Add Stock Alert</h2>
                <form onSubmit={handleSubmit}>
                    <label>Symbol:</label>
                    <select name="security_id" onChange={handleChange} required>
                        <option value="">Choose Here</option>
                        {securities.length > 0 ? (
                            securities.map((security) => (
                                <option key={security.id} value={security.id} title={security.security_name}>
                                    {security.symbol}
                                </option>
                            ))
                        ) : (
                            <option disabled>No securities available.</option>
                        )}
                    </select>

                    <label>Minimum Target Price:</label>
                    <input
                        type="number"
                        name="min_target_price"
                        value={formData.min_target_price}
                        onChange={handleChange}
                        required
                    />

                    <label>Maximum Target Price:</label>
                    <input
                        type="number"
                        name="max_target_price"
                        value={formData.max_target_price}
                        onChange={handleChange}
                        required
                    />

                    <label>Status:</label>
                    <input
                        type="checkbox"
                        name="status"
                        checked={formData.status}
                        onChange={handleChange}
                    />

                    <div className="popup-buttons">
                        <button type="button" onClick={() => setIsOpen(false)}>Cancel</button>
                        <button type="submit">Submit</button>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default PriceTrackAlertForm