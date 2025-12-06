import { useState, useEffect } from 'react'
import './GlitchText.css'

function GlitchText({ text, className = '', intense = false }) {
  const [glitchedText, setGlitchedText] = useState(text)

  useEffect(() => {
    if (!intense) {
      setGlitchedText(text)
      return
    }

    const glitchChars = '!@#$%^&*(){}[]|<>?/~`'
    const interval = setInterval(() => {
      const shouldGlitch = Math.random() > 0.7
      if (shouldGlitch) {
        const newText = text.split('').map(char => {
          if (Math.random() > 0.8) {
            return glitchChars[Math.floor(Math.random() * glitchChars.length)]
          }
          return char
        }).join('')
        setGlitchedText(newText)
      } else {
        setGlitchedText(text)
      }
    }, 100)

    return () => clearInterval(interval)
  }, [text, intense])

  return (
    <div className={`glitch-text ${className} ${intense ? 'intense-glitch' : ''}`} data-text={text}>
      {glitchedText}
    </div>
  )
}

export default GlitchText
