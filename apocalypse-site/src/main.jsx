import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import NewsletterHub from './components/NewsletterHub.jsx'
import AgentNewsletter from './components/AgentNewsletter.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/newsletter" element={<NewsletterHub />} />
        <Route path="/newsletter/:agentId" element={<AgentNewsletter />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
