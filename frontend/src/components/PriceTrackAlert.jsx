import { useState } from "react";

function PriceTrackAlert({ detail, setIsOpen }) {
    const [searchTerm, setSearchTerm] = useState("");

    // Filter alerts based on the search term
    const filteredDetails = detail.filter((alert) =>
        alert.symbol.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <>
            <div className="header-tools">
                <div className="tools">
                    <ul>
                        <li>
                            <button onClick={() => setIsOpen(true)}>
                                ➕
                            </button>
                        </li>
                    </ul>
                </div>

                <div className="search">
                    <input
                        type="search"
                        className="search-input"
                        placeholder="Search by Symbol..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>

            <table className="datatable">
                <thead>
                    <tr>
                        <th>S.N</th>
                        <th>Symbol</th>
                        <th>Minimum Price</th>
                        <th>Maximum Price</th>
                        <th>Created At</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredDetails.length > 0 ? (
                        filteredDetails.map((alert, index) => (
                            <tr key={alert.id}>
                                <td>{index + 1}</td> {/* Dynamic Serial Number */}
                                <td title={alert.name}>{alert.symbol}</td>
                                <td>{alert.min_price}</td>
                                <td>{alert.max_price}</td>
                                <td>{new Date(alert.created_at).toLocaleDateString()}</td> {/* Formatted Date */}
                                <td>{alert.status ? "Active" : "Inactive"}</td> {/* Active or Inactive Status */}
                                <td>
                                    <button>✏️</button>
                                    <button>🗑️</button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="7" className="no-data">
                                No data available.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>

            <div className="footer-tools">
                <div className="list-items">
                    Show
                    <select name="n-entries" id="n-entries" className="n-entries">
                        <option value="5">5</option>
                        <option value="10" selected>
                            10
                        </option>
                        <option value="15">15</option>
                    </select>
                    entries
                </div>

                <div className="pages">
                    <ul>
                        <li>
                            <span className="active">1</span>
                        </li>
                        <li>
                            <button>2</button>
                        </li>
                        <li>
                            <button>3</button>
                        </li>
                        <li>
                            <button>4</button>
                        </li>
                        <li>
                            <span>...</span>
                        </li>
                        <li>
                            <button>9</button>
                        </li>
                        <li>
                            <button>10</button>
                        </li>
                    </ul>
                </div>
            </div>
        </>
    );
}

export default PriceTrackAlert;
