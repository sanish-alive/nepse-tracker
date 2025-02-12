import { Route, Routes } from 'react-router-dom'
import Home from "./pages/Home"
import OpenIpo from './pages/OpenIpo'
import NavBar from './components/NavBar'
import "./styles/App.css"
import PriceTrack from './pages/PriceTrack'
import Profile from './pages/Profile'

function App() {
  return (
    <>
      <NavBar />
      <main className='main-content'>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/price-track" element={<PriceTrack />} />
          <Route path="/open-ipo" element={<OpenIpo />} />
          <Route path="profile" element={<Profile />} />
        </Routes>
      </main>
    </>
  )
}

export default App
