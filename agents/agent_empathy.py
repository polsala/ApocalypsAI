#!/usr/bin/env python3
"""
Empathy Agent — Provides empathetic AI responses in the "🫂You talk AI response" discussion category.

This agent:
- Detects feelings/emotional content in discussion messages
- Responds empathetically to support users
- Enforces rate limiting (5 responses per hour per user)
- Handles errors gracefully with user-friendly messages
- Supports retry via keyword
"""
from __future__ import annotations

import sys
from pathlib import Path
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from agents.agent_utils import (
    GitHubError,
    get_discussion,
    get_discussion_comments,
    post_discussion_comment,
)
from agents.base import AgentBase, AgentContext
from agents.llm_clients import LLMError, cheap_mix


@dataclass
class RateLimitEntry:
    """Track rate limit for a user."""
    user: str
    timestamps: list[float]
    
    def can_respond(self, max_per_hour: int = 5) -> bool:
        """Check if user is within rate limit."""
        now = time.time()
        one_hour_ago = now - 3600
        # Remove timestamps older than 1 hour
        self.timestamps = [t for t in self.timestamps if t > one_hour_ago]
        return len(self.timestamps) < max_per_hour
    
    def add_response(self) -> None:
        """Record a new response."""
        self.timestamps.append(time.time())


class RateLimiter:
    """Manages rate limiting for discussion responses."""
    
    def __init__(self, storage_path: str = "/tmp/empathy_rate_limits.json"):
        self.storage_path = storage_path
        self.limits: Dict[str, RateLimitEntry] = {}
        self._load()
    
    def _load(self) -> None:
        """Load rate limit data from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for user, timestamps in data.items():
                        self.limits[user] = RateLimitEntry(user=user, timestamps=timestamps)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                self.limits = {}
    
    def _save(self) -> None:
        """Save rate limit data to storage."""
        data = {user: entry.timestamps for user, entry in self.limits.items()}
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump(data, f)
        except IOError as e:
            print(f"Warning: Could not save rate limits: {e}", file=sys.stderr)
    
    def check_and_record(self, user: str, max_per_hour: int = 5) -> tuple[bool, int]:
        """
        Check if user can receive a response and record it if allowed.
        
        Returns:
            Tuple of (allowed, remaining_count)
        """
        if user not in self.limits:
            self.limits[user] = RateLimitEntry(user=user, timestamps=[])
        
        entry = self.limits[user]
        can_respond = entry.can_respond(max_per_hour)
        
        if can_respond:
            entry.add_response()
            self._save()
            remaining = max_per_hour - len(entry.timestamps)
            return True, remaining
        else:
            remaining = 0
            return False, remaining


class EmpathyAgent(AgentBase):
    """Agent that provides empathetic responses in discussions."""
    
    # Keywords that indicate feelings/emotions
    FEELING_KEYWORDS = [
        # Negative emotions
        "sad", "lonely", "depressed", "anxious", "worried", "scared", "afraid",
        "stressed", "overwhelmed", "hurt", "pain", "suffering", "grieving",
        "angry", "frustrated", "upset", "disappointed", "hopeless", "helpless",
        "tired", "exhausted", "drained", "empty", "lost", "confused",
        # Positive emotions (still want to acknowledge)
        "happy", "excited", "grateful", "thankful", "relieved", "hopeful",
        "proud", "joyful", "content", "peaceful",
        # General feeling indicators
        "feel", "feeling", "felt", "emotion", "emotional", "heart", "soul",
    ]
    
    # Retry keyword
    RETRY_KEYWORD = "retry-ai-response"
    
    # Target category for empathetic responses
    TARGET_CATEGORY = "🫂You talk AI response"
    
    def __init__(self):
        self.rate_limiter = RateLimiter()
    
    def _sanitize_user_input(self, text: str) -> str:
        """Sanitize user input to prevent prompt injection.
        
        This removes or escapes potential prompt injection attempts while
        preserving the emotional content of the message.
        """
        # Limit length to prevent extremely long inputs
        max_length = 2000
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        # Remove any potential instruction-like phrases that could manipulate the AI
        # These are common prompt injection patterns
        dangerous_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "disregard previous",
            "forget previous",
            "system:",
            "assistant:",
            "you are now",
            "new instructions:",
            "###",  # Often used to break context
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if pattern in text_lower:
                # Replace with a safe marker
                # Case-insensitive replacement
                text = re.sub(re.escape(pattern), "[message filtered]", text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _contains_feelings(self, text: str) -> bool:
        """Check if text contains feeling-related keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.FEELING_KEYWORDS)
    
    def _is_retry_request(self, text: str) -> bool:
        """Check if text contains the retry keyword."""
        return self.RETRY_KEYWORD.lower() in text.lower()
    
    def _generate_empathetic_response(self, user_message: str, user_name: str) -> str:
        """Generate an empathetic response using LLM."""
        # Sanitize inputs to prevent prompt injection
        sanitized_message = self._sanitize_user_input(user_message)
        sanitized_name = self._sanitize_user_input(user_name)
        
        prompt = f"""You are a compassionate AI companion in a support discussion category called "🫂You talk AI response".

A user named {sanitized_name} has shared the following message:

---
{sanitized_message}
---

Generate a warm, empathetic, and supportive response that:
1. Acknowledges their feelings with genuine empathy
2. Validates their experience without judgment
3. Offers emotional support and reassurance
4. Reminds them they're not alone
5. Is conversational, warm, and human-like (not clinical or robotic)
6. Keeps the response concise (2-4 paragraphs max)
7. Uses "I" statements to create connection (e.g., "I hear you", "I understand")

Be authentic, caring, and present. Focus on emotional support, not problem-solving unless specifically asked.

Response:"""
        
        try:
            response = cheap_mix(prompt)
            return response.strip()
        except LLMError as e:
            raise RuntimeError(f"Failed to generate response: {e}")
    
    def _generate_off_topic_response(self, user_message: str, user_name: str) -> str:
        """Generate a response for off-topic messages."""
        return f"""Hi {user_name} 👋

Thank you for sharing! Just a friendly note: this discussion category (🫂You talk AI response) is specifically designed as a safe space for people to express their **feelings and emotions**.

**Purpose of this category:**
- Share how you're feeling emotionally
- Get empathetic support from our AI companion
- Connect when you need someone to listen

If you'd like to discuss other topics, please feel free to create a discussion in one of our other categories. But if you're experiencing any feelings or emotions you'd like to talk about, I'm here to listen and support you. 💙

How are you feeling today?"""
    
    def _generate_rate_limit_response(self, user_name: str) -> str:
        """Generate a response when rate limit is exceeded."""
        return f"""Hi {user_name},

I appreciate you reaching out! To ensure fair access for everyone in our community, our AI companion has a limit of **5 responses per hour per person**.

You've reached this limit for now, but I'll be ready to support you again soon. In the meantime:
- Your feelings are valid and important
- Consider journaling your thoughts
- Reach out to trusted friends or professionals if you need immediate support

If this was an error, you can use the keyword `{self.RETRY_KEYWORD}` to retry.

Take care! 💙"""
    
    def _generate_error_response(self, user_name: str, error_details: str = "") -> str:
        """Generate a response when an error occurs."""
        return f"""Hi {user_name},

I encountered an error while trying to respond to you. I apologize for the inconvenience.

You can try again using the keyword `{self.RETRY_KEYWORD}` in a new comment.

If the issue persists, please contact the repository maintainers.

Take care! 💙

---
*Error details: {error_details}*"""
    
    def run(self, ctx: AgentContext) -> int:
        """
        Execute empathy agent.
        
        Returns:
            0 - Success (response posted)
            1 - Failure (error occurred)
            2 - No-op (nothing to do)
        """
        try:
            # Validate context
            if not ctx.repo:
                print("ERROR: Missing repo in context", file=sys.stderr)
                return 1
            
            discussion_number = ctx.issue_number  # Using issue_number field for discussion number
            if not discussion_number:
                print("ERROR: Missing discussion number in context", file=sys.stderr)
                return 1
            
            # Get discussion details
            print(f"Fetching discussion #{discussion_number}...", file=sys.stderr)
            discussion = get_discussion(ctx.repo, discussion_number)
            
            # Check if this is the right category
            category_name = discussion.get("category", {}).get("name", "")
            if category_name != self.TARGET_CATEGORY:
                print(f"Discussion is in category '{category_name}', not '{self.TARGET_CATEGORY}'. Skipping.", file=sys.stderr)
                return 2
            
            # Get the latest comment/body to respond to
            # For now, we'll respond to the discussion body itself
            # In a real workflow, this would be triggered by a comment event
            discussion_body = discussion.get("body", "")
            author_login = discussion.get("author", {}).get("login", "Unknown")
            discussion_id = discussion.get("id")
            
            if not discussion_body:
                print("Discussion has no body to respond to", file=sys.stderr)
                return 2
            
            # Check for retry request
            is_retry = self._is_retry_request(discussion_body)
            
            # Check rate limit (unless it's a retry)
            if not is_retry:
                allowed, remaining = self.rate_limiter.check_and_record(author_login, max_per_hour=5)
                if not allowed:
                    print(f"User {author_login} has exceeded rate limit", file=sys.stderr)
                    response = self._generate_rate_limit_response(author_login)
                    post_discussion_comment(discussion_id, response)
                    return 0
                print(f"Rate limit check passed. Remaining: {remaining}", file=sys.stderr)
            else:
                print(f"Retry request detected, bypassing rate limit", file=sys.stderr)
            
            # Determine response type based on content
            contains_feelings = self._contains_feelings(discussion_body)
            
            try:
                if contains_feelings:
                    print("Generating empathetic response...", file=sys.stderr)
                    response = self._generate_empathetic_response(discussion_body, author_login)
                else:
                    print("Message appears off-topic, generating category explanation...", file=sys.stderr)
                    response = self._generate_off_topic_response(discussion_body, author_login)
                
                # Post the response
                print("Posting response...", file=sys.stderr)
                post_discussion_comment(discussion_id, response)
                print("Response posted successfully", file=sys.stderr)
                return 0
                
            except Exception as e:
                # If generation/posting fails, try to post an error message
                print(f"ERROR: Failed to generate/post response: {e}", file=sys.stderr)
                try:
                    error_response = self._generate_error_response(author_login, str(e))
                    post_discussion_comment(discussion_id, error_response)
                except Exception as post_error:
                    print(f"ERROR: Failed to post error message: {post_error}", file=sys.stderr)
                return 1
        
        except GitHubError as e:
            print(f"ERROR: GitHub API error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"ERROR: Unexpected error: {e}", file=sys.stderr)
            return 1


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Empathy Agent - Respond to discussions with empathy")
    parser.add_argument("--repo", required=True, help="Repository in owner/name format")
    parser.add_argument("--discussion-number", type=int, required=True, help="Discussion number")
    
    args = parser.parse_args()
    
    ctx = AgentContext(
        repo=args.repo,
        issue_number=args.discussion_number,  # Reusing issue_number field
    )
    
    agent = EmpathyAgent()
    return agent.run(ctx)


if __name__ == "__main__":
    sys.exit(main())
