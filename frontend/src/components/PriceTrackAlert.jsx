function PriceTrackAlert({ detail }) {

    return (
        <table border="solid">
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Minimum Price</th>
                    <th>Maximum Price</th>
                    <th>Created At</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {detail.length > 0 ? (
                    detail.map((alert) => (
                        <tr key={alert.id}>
                            <td title={alert.name}>{alert.symbol}</td>
                            <td>{alert.min_price}</td>
                            <td>{alert.max_price}</td>
                            <td>{alert.created_at}</td>
                            <td>{alert.status}</td>
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan="5">No data available</td>
                    </tr>
                )}
            </tbody>
        </table>
    )
}

export default PriceTrackAlert