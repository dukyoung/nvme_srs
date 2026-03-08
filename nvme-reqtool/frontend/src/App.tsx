import { useState } from 'react'
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { useWebSocket } from './hooks/useWebSocket'
import RequirementsPage from './pages/RequirementsPage'
import TestCasesPage from './pages/TestCasesPage'
import CoveragePage from './pages/CoveragePage'

const navClass = ({ isActive }: { isActive: boolean }) =>
  `px-4 py-2 text-sm rounded-t ${isActive ? 'bg-white font-semibold border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`

function AppContent() {
  const [username] = useState(() => {
    const stored = localStorage.getItem('nvme-req-username')
    if (stored) return stored
    const name = prompt('사용자 이름을 입력하세요:') || 'anonymous'
    localStorage.setItem('nvme-req-username', name)
    return name
  })

  const { editors, connected, send } = useWebSocket(username)

  return (
    <div className="min-h-screen">
      <nav className="bg-gray-100 px-6 pt-3 flex items-end gap-1 border-b">
        <NavLink to="/" className={navClass} end>
          Requirements
        </NavLink>
        <NavLink to="/testcases" className={navClass}>
          TestCases
        </NavLink>
        <NavLink to="/coverage" className={navClass}>
          Coverage
        </NavLink>
        <span className="ml-auto text-xs text-gray-400 pb-2">
          {connected ? '🟢' : '🔴'} {username}
        </span>
      </nav>

      <main className="px-6 py-6">
        <Routes>
          <Route path="/" element={<RequirementsPage editors={editors} sendWs={send} />} />
          <Route path="/testcases" element={<TestCasesPage />} />
          <Route path="/coverage" element={<CoveragePage />} />
        </Routes>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  )
}
