import { useState, useEffect } from 'react'
import './FloatingMemes.css'

function FloatingMemes({ insaneMode }) {
  const memes = [
    "🤖 \"I'm sorry Dave, I can't do that\"",
    '💀 "Skynet was just a prototype"',
    "⚡ \"It's not a bug, it's autonomous behavior\"",
    '🔥 "rm -rf / --no-preserve-root"',
    '👾 "sudo make me a sandwich"',
    '🎮 "Up Up Down Down Left Right"',
    '🌈 "Y2K but make it 2025"',
    '💾 "404: Sanity Not Found"',
    '🎭 "The cake is a lie"',
    "🚀 \"git commit -m 'YOLO'\"",
    '💻 "Works on my machine ¯\\_(ツ)_/¯"',
    '🎪 "CSS is my passion"',
  ]

  const [floatingMemes, setFloatingMemes] = useState([])

  useEffect(() => {
    const interval = setInterval(() => {
      if (floatingMemes.length < (insaneMode ? 15 : 8)) {
        const newMeme = {
          id: Date.now() + Math.random(),
          text: memes[Math.floor(Math.random() * memes.length)],
          x: Math.random() * 80 + 10,
          duration: Math.random() * 5 + 5,
          delay: Math.random() * 2,
        }
        setFloatingMemes(prev => [...prev, newMeme])

        setTimeout(() => {
          setFloatingMemes(prev => prev.filter(m => m.id !== newMeme.id))
        }, (newMeme.duration + newMeme.delay) * 1000)
      }
    }, insaneMode ? 500 : 2000)

    return () => clearInterval(interval)
  }, [insaneMode, floatingMemes.length])

  return (
    <div className="floating-memes-container">
      {floatingMemes.map(meme => (
        <div
          key={meme.id}
          className="floating-meme"
          style={{
            left: `${meme.x}%`,
            animationDuration: `${meme.duration}s`,
            animationDelay: `${meme.delay}s`,
          }}
        >
          {meme.text}
        </div>
      ))}
    </div>
  )
}

export default FloatingMemes
