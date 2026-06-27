import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SearchPage from './pages/SearchPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <div className="container">
            <h1 className="logo">
              <span className="logo-icon">🧠</span>
              CodeMind
            </h1>
            <p className="tagline">Semantic code search powered by AI reasoning</p>
          </div>
        </header>

        <main className="app-main">
          <Routes>
            <Route path="/" element={<SearchPage />} />
          </Routes>
        </main>

        <footer className="app-footer">
          <div className="container">
            <p>
              Built with Claude AI • Not a chatbot wrapper, a reasoning engine
            </p>
          </div>
        </footer>
      </div>
    </Router>
  )
}

export default App
