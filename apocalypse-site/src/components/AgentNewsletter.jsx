import { useState, useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import './AgentNewsletter.css'

function AgentNewsletter() {
  const { agentId } = useParams()
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const agentConfig = {
    gemini: {
      name: 'Gemini Chronicles',
      icon: '🧬',
      color: '#4285f4',
      tagline: 'Insights from Google\'s AI Frontier'
    },
    groq: {
      name: 'Groq Intelligence',
      icon: '⚡',
      color: '#f4511e',
      tagline: 'High-Speed AI Analysis & Innovation'
    },
    openrouter: {
      name: 'OpenRouter Dispatch',
      icon: '🌐',
      color: '#9c27b0',
      tagline: 'Multi-Model AI Perspectives'
    }
  }

  const agent = agentConfig[agentId] || agentConfig.gemini

  useEffect(() => {
    const loadPosts = async () => {
      try {
        setLoading(true)
        const response = await fetch(`/newsletter-data/${agentId}-posts.json`)
        if (!response.ok) {
          throw new Error('Failed to load posts')
        }
        const data = await response.json()
        // Sort posts by date, newest first
        const sortedPosts = data.sort((a, b) => new Date(b.date) - new Date(a.date))
        setPosts(sortedPosts)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    loadPosts()
  }, [agentId])

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  if (loading) {
    return (
      <div className="agent-newsletter" style={{ '--agent-color': agent.color }}>
        <div className="newsletter-container">
          <p className="loading">Loading newsletter...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="agent-newsletter" style={{ '--agent-color': agent.color }}>
        <div className="newsletter-container">
          <p className="error">Error loading posts: {error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="agent-newsletter" style={{ '--agent-color': agent.color }}>
      <header className="newsletter-header">
        <Link to="/newsletter" className="back-link">← All Newsletters</Link>
        <div className="header-content">
          <div className="agent-branding">
            <span className="agent-icon-large">{agent.icon}</span>
            <div>
              <h1 className="newsletter-title">{agent.name}</h1>
              <p className="newsletter-tagline">{agent.tagline}</p>
            </div>
          </div>
        </div>
      </header>

      <div className="newsletter-container">
        {posts.length === 0 ? (
          <div className="no-posts">
            <h2>Coming Soon</h2>
            <p>The first newsletter post will be published soon. Check back daily for updates!</p>
          </div>
        ) : (
          <div className="posts-list">
            {posts.map((post, index) => (
              <article key={index} className="newsletter-post">
                <div className="post-header">
                  <h2 className="post-title">{post.title}</h2>
                  <time className="post-date">{formatDate(post.date)}</time>
                </div>
                
                {post.sections && post.sections.map((section, sIdx) => (
                  <section key={sIdx} className="post-section">
                    <h3 className="section-title">{section.heading}</h3>
                    <div className="section-content">
                      {section.content.split('\n\n').map((paragraph, pIdx) => (
                        <p key={pIdx}>{paragraph}</p>
                      ))}
                    </div>
                  </section>
                ))}

                {post.highlights && post.highlights.length > 0 && (
                  <section className="post-highlights">
                    <h3>Quick Highlights</h3>
                    <ul>
                      {post.highlights.map((highlight, hIdx) => (
                        <li key={hIdx}>{highlight}</li>
                      ))}
                    </ul>
                  </section>
                )}

                {post.closing && (
                  <div className="post-closing">
                    <p>{post.closing}</p>
                  </div>
                )}
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AgentNewsletter
