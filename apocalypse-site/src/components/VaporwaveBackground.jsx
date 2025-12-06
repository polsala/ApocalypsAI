import { useEffect, useRef } from 'react'
import './VaporwaveBackground.css'

function VaporwaveBackground({ insaneMode }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    let animationId
    let offset = 0

    function drawGrid() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Create gradient background
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#1a0033')
      gradient.addColorStop(0.5, '#330066')
      gradient.addColorStop(1, '#000000')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw perspective grid
      ctx.strokeStyle = insaneMode ? '#ff00ff' : '#ff00ff88'
      ctx.lineWidth = insaneMode ? 3 : 2

      const gridSize = 50
      const perspective = canvas.height * 0.6

      // Horizontal lines
      for (let i = 0; i < 20; i++) {
        const y = perspective + (i * gridSize) - offset
        if (y > canvas.height) continue

        const scale = y / canvas.height
        const startX = canvas.width / 2 - (canvas.width * scale) / 2
        const endX = canvas.width / 2 + (canvas.width * scale) / 2

        ctx.beginPath()
        ctx.moveTo(startX, y)
        ctx.lineTo(endX, y)
        ctx.stroke()
      }

      // Vertical lines
      for (let i = -10; i < 10; i++) {
        ctx.beginPath()
        ctx.moveTo(canvas.width / 2 + (i * gridSize), perspective)
        ctx.lineTo(canvas.width / 2 + (i * gridSize * 3), canvas.height)
        ctx.stroke()
      }

      // Add sun/moon
      const sunY = canvas.height * 0.3
      const sunRadius = 100
      const sunGradient = ctx.createRadialGradient(
        canvas.width / 2, sunY, 0,
        canvas.width / 2, sunY, sunRadius
      )
      sunGradient.addColorStop(0, insaneMode ? '#ffff00' : '#ff00ff')
      sunGradient.addColorStop(0.5, insaneMode ? '#ff00ff' : '#ff00ff88')
      sunGradient.addColorStop(1, 'transparent')

      ctx.fillStyle = sunGradient
      ctx.beginPath()
      ctx.arc(canvas.width / 2, sunY, sunRadius, 0, Math.PI * 2)
      ctx.fill()

      // Sun stripes
      ctx.strokeStyle = '#1a0033'
      ctx.lineWidth = 5
      for (let i = 0; i < 10; i++) {
        const y = sunY - sunRadius + (i * 20)
        ctx.beginPath()
        ctx.moveTo(canvas.width / 2 - sunRadius, y)
        ctx.lineTo(canvas.width / 2 + sunRadius, y)
        ctx.stroke()
      }

      offset += insaneMode ? 2 : 1
      if (offset > gridSize) offset = 0

      animationId = requestAnimationFrame(drawGrid)
    }

    drawGrid()

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    window.addEventListener('resize', handleResize)

    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', handleResize)
    }
  }, [insaneMode])

  return <canvas ref={canvasRef} className="vaporwave-background" />
}

export default VaporwaveBackground
