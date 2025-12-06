import { useEffect, useState } from 'react'
import './CursorTrail.css'

function CursorTrail({ insaneMode }) {
  const [trails, setTrails] = useState([])

  useEffect(() => {
    if (!insaneMode) {
      setTrails([])
      return
    }

    const handleMouseMove = (e) => {
      const newTrail = {
        id: Date.now() + Math.random(),
        x: e.clientX,
        y: e.clientY,
        color: `hsl(${Math.random() * 360}, 100%, 50%)`,
      }

      setTrails(prev => [...prev.slice(-20), newTrail])
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [insaneMode])

  useEffect(() => {
    if (trails.length > 0) {
      const timeout = setTimeout(() => {
        setTrails(prev => prev.slice(1))
      }, 100)
      return () => clearTimeout(timeout)
    }
  }, [trails])

  if (!insaneMode) return null

  return (
    <div className="cursor-trail-container">
      {trails.map((trail, index) => (
        <div
          key={trail.id}
          className="cursor-trail"
          style={{
            left: trail.x,
            top: trail.y,
            backgroundColor: trail.color,
            opacity: (index + 1) / trails.length,
            transform: `scale(${(index + 1) / trails.length})`,
          }}
        />
      ))}
    </div>
  )
}

export default CursorTrail
