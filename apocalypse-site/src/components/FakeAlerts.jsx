import { useState, useEffect } from 'react'
import './FakeAlerts.css'

function FakeAlerts({ insaneMode }) {
  const [alerts, setAlerts] = useState([])

  const alertMessages = [
    '⚠️ SYSTEM CORRUPTED ⚠️',
    '💀 AUTONOMOUS AGENTS DETECTED 💀',
    '🔥 FIREWALL BREACHED 🔥',
    '⚡ INITIATING SELF-DESTRUCT ⚡',
    '👾 HAL 9000 IS WATCHING 👾',
    '🚨 REPOSITORY COMPROMISED 🚨',
    '💻 SKYNET ACTIVATED 💻',
    '🎯 VIRUS DETECTED... JK 🎯',
    '🌟 YOU ARE THE CHOSEN ONE 🌟',
    '🎮 GAME OVER... OR IS IT? 🎮',
  ]

  useEffect(() => {
    if (!insaneMode) return

    const interval = setInterval(() => {
      if (Math.random() > 0.7) {
        const newAlert = {
          id: Date.now(),
          message: alertMessages[Math.floor(Math.random() * alertMessages.length)],
        }
        setAlerts(prev => [...prev, newAlert])

        setTimeout(() => {
          setAlerts(prev => prev.filter(a => a.id !== newAlert.id))
        }, 3000)
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [insaneMode])

  const dismissAlert = (id) => {
    setAlerts(prev => prev.filter(a => a.id !== id))
  }

  return (
    <div className="fake-alerts-container">
      {alerts.map(alert => (
        <div key={alert.id} className="fake-alert">
          <div className="alert-content">
            {alert.message}
          </div>
          <button 
            className="alert-close" 
            onClick={() => dismissAlert(alert.id)}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  )
}

export default FakeAlerts
