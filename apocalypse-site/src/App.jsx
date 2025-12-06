import { useState, useEffect, useRef } from 'react'
import './App.css'
import MatrixRain from './components/MatrixRain'
import GlitchText from './components/GlitchText'
import FloatingMemes from './components/FloatingMemes'
import FakeAlerts from './components/FakeAlerts'
import CursorTrail from './components/CursorTrail'
import AsciiArt from './components/AsciiArt'
import Countdown from './components/Countdown'
import TerminalSection from './components/TerminalSection'
import VaporwaveBackground from './components/VaporwaveBackground'
import ExplosionEffect from './components/ExplosionEffect'

function App() {
  const [insaneMode, setInsaneMode] = useState(false)
  const [glitchLevel, setGlitchLevel] = useState(1)
  const [showEasterEgg, setShowEasterEgg] = useState(false)
  const [explosions, setExplosions] = useState([])
  const audioRef = useRef(null)

  useEffect(() => {
    // Random color cycling
    const colorInterval = setInterval(() => {
      if (insaneMode) {
        document.documentElement.style.setProperty(
          '--chaos-color',
          `hsl(${Math.random() * 360}, 100%, 50%)`
        )
      }
    }, 100)

    // Random layout shifts in insane mode
    const layoutInterval = setInterval(() => {
      if (insaneMode) {
        const rotation = Math.random() * 10 - 5
        document.body.style.transform = `rotate(${rotation}deg)`
      } else {
        document.body.style.transform = 'rotate(0deg)'
      }
    }, 2000)

    return () => {
      clearInterval(colorInterval)
      clearInterval(layoutInterval)
    }
  }, [insaneMode])

  useEffect(() => {
    // Random events on page load
    const events = [
      () => setGlitchLevel(Math.floor(Math.random() * 3) + 1),
      () => {
        setTimeout(() => {
          setShowEasterEgg(true)
          setTimeout(() => setShowEasterEgg(false), 3000)
        }, Math.random() * 5000)
      }
    ]
    
    events.forEach(event => event())
  }, [])

  const createExplosion = (e) => {
    const newExplosion = {
      id: Date.now(),
      x: e.clientX,
      y: e.clientY
    }
    setExplosions(prev => [...prev, newExplosion])
    setTimeout(() => {
      setExplosions(prev => prev.filter(exp => exp.id !== newExplosion.id))
    }, 1000)
  }

  const toggleInsaneMode = () => {
    setInsaneMode(!insaneMode)
    if (!insaneMode && audioRef.current) {
      audioRef.current.play().catch(() => {})
    }
  }

  const konami = useRef([])
  useEffect(() => {
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a']
    
    const handleKeyDown = (e) => {
      konami.current.push(e.key)
      konami.current = konami.current.slice(-10)
      
      if (konami.current.join(',') === konamiCode.join(',')) {
        setInsaneMode(true)
        alert('🎮 KONAMI CODE ACTIVATED! MAXIMUM CHAOS ENGAGED! 🎮')
      }
    }
    
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <div className={`app-container ${insaneMode ? 'insane-mode' : ''} glitch-level-${glitchLevel}`} onClick={createExplosion}>
      <MatrixRain />
      <VaporwaveBackground insaneMode={insaneMode} />
      <CursorTrail insaneMode={insaneMode} />
      
      {explosions.map(exp => (
        <ExplosionEffect key={exp.id} x={exp.x} y={exp.y} />
      ))}

      <header className="chaos-header">
        <GlitchText text="APOCALYPSAI" className="main-title" intense={insaneMode} />
        <p className="tagline">
          <span className="rotating-text">WHERE AI AGENTS GO TO DIE</span>
          <span className="blink"> █</span>
        </p>
      </header>

      <div className="insane-mode-toggle">
        <button onClick={toggleInsaneMode} className="chaos-button">
          {insaneMode ? '🔥 STOP THE MADNESS 🔥' : '😈 ACTIVATE INSANE MODE 😈'}
        </button>
      </div>

      <Countdown />

      <section className="warning-section">
        <div className="warning-box">
          <h2>⚠️ SYSTEM ALERT ⚠️</h2>
          <p>AUTONOMOUS AGENTS DETECTED</p>
          <p>REPOSITORY INTEGRITY: <span className="critical">COMPROMISED</span></p>
          <p>SANITY LEVEL: <span className="blink">UNDEFINED</span></p>
          <div className="progress-bar">
            <div className="progress-fill chaos-fill"></div>
          </div>
        </div>
      </section>

      <AsciiArt />

      <section className="features-section">
        <h2 className="section-title">
          <GlitchText text="THE CHAOS COLLECTIVE" />
        </h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>🤖 BUILDER AGENT</h3>
            <p>Materializes utilities from the void. Accepts GitHub issues. Outputs chaos.</p>
            <code className="fake-code">{"while(true) { create(); deploy(); }"}</code>
          </div>
          <div className="feature-card">
            <h3>👁️ REVIEWER AGENT</h3>
            <p>Multi-provider AI overlord. Reviews your code. Judges your soul.</p>
            <code className="fake-code">{"if(pr.quality < threshold) reject();"}</code>
          </div>
          <div className="feature-card">
            <h3>🛡️ GUARDIAN AGENT</h3>
            <p>Content safety triage. Blocks the forbidden. Protects the repository.</p>
            <code className="fake-code">{"scan(issue); classify(); block();"}</code>
          </div>
          <div className="feature-card">
            <h3>🌙 INTEGRATOR AGENT</h3>
            <p>Nightly surprise generator. Creates utilities while you sleep.</p>
            <code className="fake-code">{"at(2:42am) { surprise(); }"}</code>
          </div>
        </div>
      </section>

      <TerminalSection />

      <section className="meme-section">
        <h2 className="section-title">HALL OF MEMES</h2>
        <FloatingMemes insaneMode={insaneMode} />
      </section>

      <section className="tech-section">
        <div className="tech-grid">
          <div className="tech-item">
            <span className="tech-icon">🐍</span>
            <span>Python 3.11</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">🦀</span>
            <span>Rust</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">⚡</span>
            <span>Go</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">📜</span>
            <span>Bash</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">⚛️</span>
            <span>React</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">🟦</span>
            <span>TypeScript</span>
          </div>
        </div>
      </section>

      <section className="repo-section">
        <h2 className="section-title">
          <GlitchText text="ENTER THE APOCALYPSE" />
        </h2>
        <a 
          href="https://github.com/polsala/ApocalypsAI" 
          target="_blank" 
          rel="noopener noreferrer"
          className="github-button"
        >
          🚀 VISIT THE REPOSITORY 🚀
        </a>
        <p className="disclaimer">Warning: May contain autonomous agents, wild code generation, and unexpected PRs</p>
      </section>

      <FakeAlerts insaneMode={insaneMode} />

      {showEasterEgg && (
        <div className="easter-egg">
          <h1>🎉 YOU FOUND AN EASTER EGG! 🎉</h1>
          <p>Secret Code: HAL-9000-SAYS-HELLO</p>
        </div>
      )}

      <footer className="chaos-footer">
        <p>ApocalypsAI © {new Date().getFullYear()} - Where Anarchy Meets Discipline</p>
        <p className="footer-chaos">
          <span className="blink">⚡</span> Powered by Chaos, Caffeine, and LLMs <span className="blink">⚡</span>
        </p>
        <div className="footer-links">
          <a href="#" onClick={(e) => { e.preventDefault(); alert('🎭 You clicked a mysterious link!'); }}>???</a>
          <span>•</span>
          <a href="#" onClick={(e) => { e.preventDefault(); window.location.href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'; }}>SECRET</a>
          <span>•</span>
          <a href="#" onClick={(e) => { e.preventDefault(); setGlitchLevel((glitchLevel % 3) + 1); }}>GLITCH</a>
        </div>
      </footer>

      <audio ref={audioRef} loop>
        <source src="/sounds/apocalypse.mp3" type="audio/mpeg" />
      </audio>
    </div>
  )
}

export default App
