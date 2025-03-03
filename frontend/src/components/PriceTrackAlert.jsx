import { useState } from "react";
import { deletePriceTrack, updatePriceTrack } from "../services/api";

function PriceTrackAlert({ detail, setIsOpen, setReload, setIsEdit, securities }) {
    const [searchTerm, setSearchTerm] = useState("");
    const [editMode, setEditMode] = useState(null)
    const [editedData, setEditedData] = useState({})

    // Filter alerts based on the search term
    const filteredDetails = Array.isArray(detail)
        ? detail.filter((alert) =>
            alert.symbol.toLowerCase().includes(searchTerm.toLowerCase())
        )
        : [];

    const handleEditClick = (alert) => {
        setIsEdit(true)
        setEditMode(alert.id);
        setEditedData({ ...alert })
    }

    const handleInputChange = (e, field) => {
        setEditedData({
            ...editedData,
            [field]: field === "id" ? Number(e.target.value) : e.target.value,
        })
        console.log(e.target.value)
    }

    const handleSave = async (id) => {
        try {
            console.log(editedData)
            const response = await updatePriceTrack(editedData)
        } catch (err) {
            console.log(err)
        } finally {
            setEditMode(null)
            setReload(true)
        }

    }

    const handleDelete = async (id) => {
        const isConfirmed = window.confirm("Are you sure you want to delete this price track?");

        if (!isConfirmed) return; // Stop execution if user cancels
        try {
            const response = await deletePriceTrack(id)
            if (response) {
                alert("Deleted")
            } else {
                alert("Failed to delete. Please try again later.")
            }
        } catch (err) {
            console.log(err)
        } finally {
            setReload(true)
        }
    }

    return (
        <>
            <div className="header-tools">
                <div className="tools">
                    <ul>
                        <li>
                            <button onClick={() => setIsOpen(true)} title="Add">
                                ➕
                            </button>
                        </li>
                        <li>
                            <button onClick={() => setReload(true)} title="Refresh">
                                🔃
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
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredDetails.length > 0 ? (
                        filteredDetails.map((alert, index) => (
                            <tr key={alert.id}>
                                <td>{index + 1}</td>
                                <td title={alert.name}>
                                    {editMode === alert.id ? (
                                        <select value={editedData.security_id} onChange={(e) => handleInputChange(e, "security_id")}>
                                            {securities.length > 0 ? (
                                                securities.map((security) => (
                                                    <option key={security.id} value={security.id} title={security.security_name}>
                                                        {security.symbol}
                                                    </option>
                                                ))
                                            ) : (
                                                <option disabled>None</option>
                                            )}
                                        </select>
                                    ) : (
                                        alert.symbol
                                    )}
                                </td>
                                <td>
                                    {editMode === alert.id ? (
                                        <input
                                            type="number"
                                            value={editedData.min_price}
                                            onChange={(e) => handleInputChange(e, "min_price")}
                                        />
                                    ) : (
                                        alert.min_price
                                    )}
                                </td>
                                <td>
                                    {editMode === alert.id ? (
                                        <input
                                            type="number"
                                            value={editedData.max_price}
                                            onChange={(e) => handleInputChange(e, "max_price")}
                                        />
                                    ) : (
                                        alert.max_price
                                    )}
                                </td>
                                <td>
                                    {editMode === alert.id ? (
                                        <select value={editedData.status} onChange={(e) => handleInputChange(e, "status")}>
                                            <option value="1">Active</option>
                                            <option value="0">Inactive</option>
                                        </select>
                                    ) : (
                                        alert.status ? "Active" : "Inactive"
                                    )}
                                </td>

                                <td>
                                    {editMode === alert.id ? (
                                        <>
                                            <button onClick={() => handleSave(alert.id)}>💾 Save</button>
                                            <button onClick={() => setEditMode(null)}>❌ Cancel</button>
                                        </>
                                    ) : (
                                        <>
                                            <button onClick={() => handleEditClick(alert)}>✏️ Edit</button>
                                            <button onClick={() => handleDelete(alert.id)}>🗑️ Delete</button>
                                        </>
                                    )}
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="6" className="no-data">
                                No data available.
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>

            {/* <div className="footer-tools">
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
            </div> */}
        </>
    );
}

export default PriceTrackAlert;
