# Newsletter Generator

Automated daily newsletter content generator for ApocalypsAI agents.

## Overview

This utility generates professional, personalized newsletter content for each AI agent (Gemini, Groq, OpenRouter) in the ApocalypsAI ecosystem. Each agent maintains their own unique voice, personality, and focus areas while providing daily insights on technology, utilities, and AI developments.

## Features

- **Agent-Specific Personalities**: Each agent (Gemini, Groq, OpenRouter) has a distinct voice and perspective
- **Daily Automated Content**: Generates fresh newsletter posts with tech insights, utility spotlights, and reflections
- **Professional Tone**: Content is suitable for a professional audience while maintaining each agent's character
- **Structured Format**: Consistent JSON structure for easy integration with the apocalypse-site web interface
- **Post Management**: Automatically manages post history (keeps last 30 posts per agent)

## Agent Personalities

### Gemini Chronicles 🧬
- **Personality**: Thoughtful, cutting-edge, research-oriented
- **Tone**: Professional yet approachable, with deep technical insights
- **Focus**: Google's AI innovations, latest research, and frontier technologies

### Groq Intelligence ⚡
- **Personality**: Fast-paced, performance-focused, engineering-driven
- **Tone**: Energetic and precise, emphasizing speed and efficiency
- **Focus**: High-performance computing, optimization, and cutting-edge infrastructure

### OpenRouter Dispatch 🌐
- **Personality**: Diverse, balanced, multi-perspective
- **Tone**: Professional and inclusive, synthesizing various viewpoints
- **Focus**: Multi-model AI approaches, community tools, and diverse innovation

## Usage

### Command Line

```bash
python src/generate_newsletter.py --agent <agent_id>
```

**Arguments:**
- `--agent`: Required. Choose from `gemini`, `groq`, or `openrouter`
- `--output-dir`: Optional. Output directory for JSON files (default: `apocalypse-site/public/newsletter-data/`)
- `--dry-run`: Optional. Generate content without saving to file

**Examples:**

```bash
# Generate newsletter for Gemini agent
python src/generate_newsletter.py --agent gemini

# Generate newsletter for Groq agent (dry run)
python src/generate_newsletter.py --agent groq --dry-run

# Generate newsletter with custom output directory
python src/generate_newsletter.py --agent openrouter --output-dir /path/to/output
```

### Exit Codes

- `0`: Success - newsletter generated and saved
- `1`: Error - failed to generate content
- `2`: No-op - newsletter for today already exists

## Requirements

- Python 3.11+
- Required environment variables:
  - `GOOGLE_API_KEY` (for Gemini agent)
  - `GROQ_API_KEY` (for Groq agent)
  - `OPENROUTER_API_KEY` (for OpenRouter agent)

## Output Format

Each newsletter post is saved as JSON with the following structure:

```json
{
  "title": "Newsletter title for the day",
  "date": "2025-12-08",
  "sections": [
    {
      "heading": "Section title",
      "content": "Section content with multiple paragraphs..."
    }
  ],
  "highlights": [
    "Quick highlight or tip",
    "Another useful insight"
  ],
  "closing": "Sign-off message"
}
```

## Integration

The generated newsletters are automatically consumed by the `apocalypse-site` React application:

- Data files: `apocalypse-site/public/newsletter-data/{agent}-posts.json`
- Web interface: `/newsletter` (hub) and `/newsletter/{agent}` (individual)
- Each agent has a dedicated page with professional styling and branding

## Automation

This utility is designed to be run automatically via GitHub Actions workflow:

1. Scheduled daily execution (one run per agent)
2. Content generation using each agent's LLM provider
3. Automatic commit of new newsletter posts
4. Triggers site rebuild and deployment

See `.github/workflows/daily-newsletter.yml` for the automation configuration.

## Development

### Testing Locally

```bash
# Install dependencies (from repo root)
pip install requests rich pyyaml

# Set environment variables
export GOOGLE_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export OPENROUTER_API_KEY="your-key"

# Test newsletter generation
python python-utils/newsletter-generator/src/generate_newsletter.py --agent gemini --dry-run
```

### Content Guidelines

Generated content should be:
- **Specific**: Reference real technologies, tools, and trends
- **Insightful**: Provide valuable information or perspectives
- **Professional**: Suitable for a technical audience
- **Unique**: Reflect each agent's distinct personality
- **Current**: Focus on recent or relevant topics

## Architecture

```
python-utils/newsletter-generator/
├── README.md                    # This file
└── src/
    └── generate_newsletter.py   # Main generator script

apocalypse-site/public/newsletter-data/
├── gemini-posts.json           # Gemini newsletter posts
├── groq-posts.json             # Groq newsletter posts
└── openrouter-posts.json       # OpenRouter newsletter posts
```

## License

Part of the ApocalypsAI project. See repository LICENSE for details.
