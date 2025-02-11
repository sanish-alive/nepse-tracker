function PriceTrackAlert({ detail }) {
    function onAlertClick() {
        alert("clicked")
    }

    return (
        <div className="alert-card">
            <div className="alert-poster">
                <div className="alert-detail">
                    <p>{detail.symbol}</p>
                    <p>{detail.min_price}</p>
                    <p>{detail.max_price}</p>
                    <p>{detail.created_at}</p>
                </div>
                <div className="alert-overlay">
                    <button className="alert-button" onClick={onAlertClick}>💗</button>
                </div>
            </div>
        </div>
    )
}

export default PriceTrackAlert