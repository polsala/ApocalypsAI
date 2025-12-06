import { useEffect, useState } from 'react'
import './ExplosionEffect.css'

function ExplosionEffect({ x, y }) {
  const [particles, setParticles] = useState([])

  useEffect(() => {
    const newParticles = []
    for (let i = 0; i < 20; i++) {
      const angle = (Math.PI * 2 * i) / 20
      const velocity = Math.random() * 5 + 5
      newParticles.push({
        id: i,
        x: 0,
        y: 0,
        vx: Math.cos(angle) * velocity,
        vy: Math.sin(angle) * velocity,
        color: `hsl(${Math.random() * 360}, 100%, 50%)`,
        size: Math.random() * 10 + 5,
      })
    }
    setParticles(newParticles)
  }, [])

  return (
    <div className="explosion-container" style={{ left: x, top: y }}>
      {particles.map(particle => (
        <div
          key={particle.id}
          className="explosion-particle"
          style={{
            '--vx': `${particle.vx}px`,
            '--vy': `${particle.vy}px`,
            backgroundColor: particle.color,
            width: particle.size,
            height: particle.size,
          }}
        />
      ))}
    </div>
  )
}

export default ExplosionEffect
