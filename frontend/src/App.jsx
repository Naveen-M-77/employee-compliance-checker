import { Routes, Route, Link } from 'react-router-dom'
import { useState } from 'react'
import PredictionForm from './components/PredictionForm'
import BlockchainViewer from './components/BlockchainViewer'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>Employee Compliance Prediction</h1>
        <nav>
          <Link to="/" className="nav-link">Prediction</Link>
          <Link to="/blockchain" className="nav-link">Blockchain</Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<PredictionForm />} />
          <Route path="/blockchain" element={<BlockchainViewer />} />
        </Routes>
      </main>

      <footer>
        <p>Employee Compliance Prediction System &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  )
}

export default App