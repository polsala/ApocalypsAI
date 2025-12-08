#!/usr/bin/env python3
"""
Newsletter Generator for ApocalypsAI Agents

Generates daily newsletter content for each agent (Gemini, Groq, OpenRouter)
with professional, personalized content about technology, utilities, and insights.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add agents directory to path for LLM clients
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.llm_clients import LLMError, call_gemini, call_groq, call_openrouter


AGENT_CONFIGS = {
    "gemini": {
        "name": "Gemini Chronicles",
        "provider": "gemini",
        "personality": "thoughtful, cutting-edge, research-oriented",
        "tone": "professional yet approachable, with deep technical insights",
        "focus": "Google's AI innovations, latest research, and frontier technologies"
    },
    "groq": {
        "name": "Groq Intelligence",
        "provider": "groq",
        "personality": "fast-paced, performance-focused, engineering-driven",
        "tone": "energetic and precise, emphasizing speed and efficiency",
        "focus": "high-performance computing, optimization, and cutting-edge infrastructure"
    },
    "openrouter": {
        "name": "OpenRouter Dispatch",
        "provider": "openrouter",
        "personality": "diverse, balanced, multi-perspective",
        "tone": "professional and inclusive, synthesizing various viewpoints",
        "focus": "multi-model AI approaches, community tools, and diverse innovation"
    }
}


def generate_newsletter_prompt(agent_id: str, date: str) -> str:
    """Generate prompt for newsletter content based on agent personality."""
    config = AGENT_CONFIGS[agent_id]
    
    prompt = f"""You are writing a daily newsletter called "{config['name']}" for {date}.

PERSONALITY: {config['personality']}
TONE: {config['tone']}
FOCUS AREAS: {config['focus']}

Write a professional newsletter post with the following structure (return ONLY valid JSON):

{{
  "title": "An engaging, specific title for today's newsletter",
  "date": "{date}",
  "sections": [
    {{
      "heading": "Tech Insight of the Day",
      "content": "A 2-3 paragraph insight about a current technology trend, innovation, or development. Be specific and insightful."
    }},
    {{
      "heading": "Utility Spotlight",
      "content": "Highlight a useful tool, library, or utility (from ApocalypsAI or the broader tech ecosystem). Explain what it does and why it matters."
    }},
    {{
      "heading": "Personal Reflection",
      "content": "A brief reflection on AI, automation, software development, or technology from your unique perspective as a {agent_id} agent."
    }}
  ],
  "highlights": [
    "3-5 bullet point highlights or quick tips",
    "Each should be concise and actionable",
    "Technology news, tools, or insights"
  ],
  "closing": "A brief, professional sign-off message"
}}

REQUIREMENTS:
- Be specific and informative, not generic
- Include real technologies, concepts, or trends
- Write in the specified tone and personality
- Keep content professional and valuable
- Focus on software development, AI, automation, and technology
- Return ONLY the JSON object, no additional text

Generate the newsletter content now:"""

    return prompt


def generate_newsletter_content(agent_id: str) -> Dict:
    """Generate newsletter content for a specific agent."""
    config = AGENT_CONFIGS[agent_id]
    date = datetime.now().strftime("%Y-%m-%d")
    
    prompt = generate_newsletter_prompt(agent_id, date)
    
    # Call the appropriate LLM provider
    try:
        if config["provider"] == "gemini":
            response = call_gemini(prompt)
        elif config["provider"] == "groq":
            response = call_groq(prompt)
        elif config["provider"] == "openrouter":
            response = call_openrouter(prompt)
        else:
            raise ValueError(f"Unknown provider: {config['provider']}")
        
        # Parse JSON response
        # Remove markdown code fences if present
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        content = json.loads(response)
        return content
        
    except (LLMError, json.JSONDecodeError, ValueError) as e:
        print(f"ERROR generating content for {agent_id}: {e}", file=sys.stderr)
        raise


def load_existing_posts(posts_file: Path) -> list:
    """Load existing posts from JSON file."""
    if posts_file.exists():
        with open(posts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_posts(posts_file: Path, posts: list) -> None:
    """Save posts to JSON file."""
    posts_file.parent.mkdir(parents=True, exist_ok=True)
    with open(posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Generate newsletter content for ApocalypsAI agents")
    parser.add_argument(
        "--agent",
        choices=list(AGENT_CONFIGS.keys()),
        required=True,
        help="Agent to generate newsletter for"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "apocalypse-site" / "public" / "newsletter-data",
        help="Output directory for newsletter JSON files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate content but don't save to file"
    )
    
    args = parser.parse_args()
    
    # Generate content
    print(f"Generating newsletter for {args.agent}...")
    try:
        content = generate_newsletter_content(args.agent)
    except Exception as e:
        print(f"Failed to generate content: {e}", file=sys.stderr)
        return 1
    
    if args.dry_run:
        print("DRY RUN - Generated content:")
        print(json.dumps(content, indent=2))
        return 0
    
    # Load existing posts
    posts_file = args.output_dir / f"{args.agent}-posts.json"
    posts = load_existing_posts(posts_file)
    
    # Check if we already have a post for today
    today = datetime.now().strftime("%Y-%m-%d")
    if any(post.get('date') == today for post in posts):
        print(f"Newsletter for {today} already exists for {args.agent}")
        return 2
    
    # Add new post to the beginning
    posts.insert(0, content)
    
    # Keep only the last 30 posts
    posts = posts[:30]
    
    # Save posts
    save_posts(posts_file, posts)
    print(f"Newsletter saved to {posts_file}")
    print(f"Total posts: {len(posts)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
