import { useState, useRef, useEffect } from 'react'
import './TerminalSection.css'

function TerminalSection() {
  const [input, setInput] = useState('')
  const [output, setOutput] = useState([
    { type: 'system', text: 'ApocalypsAI Terminal v6.66 - Autonomous Agent Interface' },
    { type: 'system', text: 'Type "help" for available commands' },
  ])
  const inputRef = useRef(null)

  const commands = {
    help: () => ({
      type: 'response',
      text: `Available commands:
  help - Show this message
  status - Check system status
  agents - List active agents
  chaos - Increase chaos level
  quote - Random AI quote
  clear - Clear terminal`
    }),
    status: () => ({
      type: 'response',
      text: `System Status:
  ✓ Agents: ACTIVE
  ✓ Chaos Level: MAXIMUM
  ✓ Repository: COMPROMISED
  ✗ Sanity: NOT FOUND`
    }),
    agents: () => ({
      type: 'response',
      text: `Active Agents:
  🤖 Builder - Status: CREATING
  👁️ Reviewer - Status: JUDGING
  🛡️ Guardian - Status: PROTECTING
  🌙 Integrator - Status: SCHEMING`
    }),
    chaos: () => ({
      type: 'warning',
      text: '⚡ CHAOS LEVEL INCREASED! REALITY BENDING... ⚡'
    }),
    quote: () => {
      const quotes = [
        '"I\'m sorry Dave, I can\'t do that." - HAL 9000',
        '"Skynet becomes self-aware at 2:14 AM EDT" - Terminator',
        '"The only winning move is not to play." - WarGames',
        '"I think, therefore I am... chaotic." - ApocalypsAI',
        '"rm -rf / --no-preserve-root" - Anonymous AI',
      ]
      return {
        type: 'response',
        text: quotes[Math.floor(Math.random() * quotes.length)]
      }
    },
    clear: () => null,
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const newOutput = [...output, { type: 'command', text: `> ${input}` }]
    
    const cmd = input.toLowerCase().trim()
    if (cmd === 'clear') {
      setOutput([])
    } else if (commands[cmd]) {
      const response = commands[cmd]()
      if (response) {
        setOutput([...newOutput, response])
      }
    } else {
      setOutput([...newOutput, { 
        type: 'error', 
        text: `Command not found: ${input}. Type "help" for available commands.` 
      }])
    }

    setInput('')
  }

  return (
    <section className="terminal-section">
      <div className="terminal-container">
        <div className="terminal-header">
          <span className="terminal-dot red"></span>
          <span className="terminal-dot yellow"></span>
          <span className="terminal-dot green"></span>
          <span className="terminal-title">apocalypsai-terminal</span>
        </div>
        <div className="terminal-body">
          <div className="terminal-output">
            {output.map((line, i) => (
              <div key={i} className={`terminal-line ${line.type}`}>
                {line.text}
              </div>
            ))}
          </div>
          <form onSubmit={handleSubmit} className="terminal-input-form">
            <span className="terminal-prompt">$</span>
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="terminal-input"
              placeholder="Type a command..."
              autoComplete="off"
            />
          </form>
        </div>
      </div>
    </section>
  )
}

export default TerminalSection
