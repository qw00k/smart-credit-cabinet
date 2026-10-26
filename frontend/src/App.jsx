import { Link, Routes, Route, Navigate } from 'react-router-dom'
import LichnyiKabinet from './pages/ClientDashboard'
import AdminkaBanka from './pages/BankAdmin'

export default function App() {
  return (
    <div>
      <div className="container nav">
        <Link to="/client">Клиент</Link>
        <Link to="/bank">Банк</Link>
      </div>
      <Routes>
        <Route path="/" element={<Navigate to="/client" />} />
        <Route path="/client" element={<LichnyiKabinet />} />
        <Route path="/bank" element={<AdminkaBanka />} />
      </Routes>
    </div>
  )
}
