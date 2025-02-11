import { Route, Routes } from 'react-router-dom'
import Home from "./pages/Home"
import OpenIpo from './pages/OpenIpo'
import NavBar from './components/NavBar'
import "./styles/App.css"
import PriceTrack from './pages/PriceTrack'

function App() {
  return (
    <>
      <NavBar />
      <main className='main-content'>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/price-track" element={<PriceTrack />} />
          <Route path="/open-ipo" element={<OpenIpo />} />
        </Routes>
      </main>
    </>
  )
}

export default App
