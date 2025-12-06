import { useState, useEffect } from 'react'
import './Countdown.css'

function Countdown() {
  const [time, setTime] = useState(600) // 10 minutes in seconds
  const [message, setMessage] = useState('SYSTEM MELTDOWN IN')

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(prev => {
        if (prev <= 1) {
          setMessage('💥 MELTDOWN COMPLETE 💥')
          return 600 // Reset
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(interval)
  }, [])

  const minutes = Math.floor(time / 60)
  const seconds = time % 60

  return (
    <div className="countdown-section">
      <div className="countdown-container">
        <h3 className="countdown-title">{message}</h3>
        <div className="countdown-display">
          <div className="countdown-segment">
            <div className="countdown-number">{String(minutes).padStart(2, '0')}</div>
            <div className="countdown-label">MIN</div>
          </div>
          <div className="countdown-colon">:</div>
          <div className="countdown-segment">
            <div className="countdown-number">{String(seconds).padStart(2, '0')}</div>
            <div className="countdown-label">SEC</div>
          </div>
        </div>
        <p className="countdown-warning">⚠️ Just kidding... or are we? ⚠️</p>
      </div>
    </div>
  )
}

export default Countdown
