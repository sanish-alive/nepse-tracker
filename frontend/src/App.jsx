import { Route, Routes } from 'react-router-dom'
import Home from "./pages/Home"
import OpenIpo from './pages/OpenIpo'
import NavBar from './components/NavBar'
import "./styles/App.css"
import PriceTrack from './pages/PriceTrack'
import Profile from './pages/Profile'
import Login from './pages/Login'
import { AuthProvider } from './context/AuthContext'

function App() {
  return (
    <AuthProvider>
      <NavBar />
      <main className='main-content'>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/price-track" element={<PriceTrack />} />
          <Route path="/open-ipo" element={<OpenIpo />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </main>
    </AuthProvider>
  )
}

export default App
