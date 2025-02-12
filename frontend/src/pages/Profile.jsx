import { useState, useEffect } from "react"
import { getProfile } from "../services/api"

function Profile() {
    const [profile, setProfile] = useState([])
    useEffect(() => {
        const myProfile = async () => {
            try {
                const data = await getProfile()
                setProfile(data)
            } catch (err) {
                console.log(err)
            }   
        }
        myProfile()
    },[])

    return (
        <div className="profile-container">
            <p>Name: {profile.username}</p>
            <p>Full Name: {profile.fullname}</p>
            <p>Email: {profile.email}</p>
        </div>
    )
}

export default Profile