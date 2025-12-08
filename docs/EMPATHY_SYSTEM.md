# Empathetic AI Response System

## Overview

The Empathetic AI Response System is a compassionate AI companion that provides emotional support to users in the **🫂You talk AI response** discussion category. The system is designed to create a safe, supportive space where community members can express their feelings and receive empathetic responses.

## Purpose and Objectives

### Primary Goals
- **Emotional Support**: Provide a listening ear and empathetic responses to users sharing their feelings
- **Safe Space**: Create a judgment-free environment where users feel comfortable expressing emotions
- **Community Wellbeing**: Support mental and emotional health within the community
- **Accessibility**: Ensure fair access through rate limiting while maintaining responsiveness

### What the System Does
- Automatically detects when users share feelings or emotions
- Responds with warm, empathetic, and supportive messages
- Guides users to the appropriate category if discussions are off-topic
- Maintains fair access through rate limiting
- Handles errors gracefully with user-friendly messages

## Empathetic Response Principles

The AI companion follows these principles when responding:

### 1. **Genuine Empathy**
- Acknowledges feelings with authentic care and understanding
- Uses "I" statements to create connection (e.g., "I hear you", "I understand")
- Validates experiences without judgment or dismissal

### 2. **Emotional Validation**
- Recognizes that all feelings are valid and important
- Avoids minimizing or comparing experiences
- Creates space for users to be heard and understood

### 3. **Supportive Presence**
- Reminds users they're not alone
- Offers reassurance without false promises
- Maintains a warm, conversational tone (not clinical or robotic)

### 4. **Respect for Boundaries**
- Focuses on emotional support, not problem-solving (unless specifically asked)
- Keeps responses concise (2-4 paragraphs)
- Redirects off-topic discussions gently and respectfully

### 5. **Human-Like Connection**
- Uses natural, conversational language
- Expresses care through tone and word choice
- Balances professionalism with warmth

## How It Works

### Sentiment Detection

The system automatically detects feelings-related content using keyword analysis. It recognizes:

**Negative Emotions:**
- Sadness: sad, lonely, depressed, hopeless
- Anxiety: anxious, worried, scared, afraid, stressed, overwhelmed
- Pain: hurt, pain, suffering, grieving
- Anger: angry, frustrated, upset, disappointed
- Exhaustion: tired, exhausted, drained, empty, lost, confused

**Positive Emotions:**
- Joy: happy, excited, joyful, content, peaceful
- Gratitude: grateful, thankful, relieved
- Hope: hopeful, proud

**General Indicators:**
- feel, feeling, felt, emotion, emotional, heart, soul

### Response Generation

Based on the detected content, the system generates one of three response types:

#### 1. Empathetic Response (for feelings-related messages)
Generated when the user is sharing emotions or feelings. The response:
- Acknowledges their specific feelings
- Validates their experience
- Offers emotional support
- Reminds them they're not alone
- Uses a warm, conversational tone

#### 2. Off-Topic Guidance (for non-feelings messages)
Generated when the message doesn't contain feeling-related content. The response:
- Thanks the user for sharing
- Gently explains the category's purpose
- Invites them to discuss other topics in appropriate categories
- Asks if they have any feelings they'd like to share

#### 3. Error Response
Generated when technical issues occur. The response:
- Acknowledges the error
- Provides information about the retry mechanism
- Maintains a supportive tone despite the technical issue

## Rate Limiting Mechanism

### Purpose
Rate limiting ensures fair access to the AI companion for all community members and prevents system abuse.

### Limits
- **5 responses per hour per user**
- Rate limits reset on a rolling 1-hour window
- Limits apply per GitHub username

### How It Works
1. Each time a user posts, the system checks their recent response history
2. If the user has received fewer than 5 responses in the past hour, a response is generated
3. If the limit is reached, a friendly rate limit message is posted instead
4. The system tracks timestamps and automatically clears old entries after 1 hour

### Rate Limit Message
When the limit is reached, users receive a message that:
- Explains the rate limit policy
- Reassures them that their feelings are valid
- Suggests alternative support options
- Mentions the retry mechanism for errors

### Storage
Rate limit data is stored in `/tmp/empathy_rate_limits.json` and persists across workflow runs within the same runner session.

## Error Handling Strategy

### Error Types

#### 1. API Errors
- **GitHub API failures**: Network issues, authentication problems
- **LLM API failures**: Provider unavailable, quota exceeded

#### 2. Rate Limit Errors
- User exceeds 5 responses per hour
- Handled gracefully with informative message

#### 3. Configuration Errors
- Missing required parameters
- Invalid discussion category

### Error Response Behavior

When errors occur, the system:
1. **Logs the error** to stderr for debugging
2. **Attempts to post a user-friendly error message** explaining what happened
3. **Mentions the retry keyword** so users can try again
4. **Includes error details** (sanitized) for transparency
5. **Exits with appropriate code** (1 for failure, 2 for no-op)

### Graceful Degradation

If the system cannot post an error message:
- Logs to stderr for workflow visibility
- Exits with error code 1
- Does not crash or hang

## Retry System

### Purpose
The retry system allows users to request a new AI response if an error occurred or they want to reformulate their message.

### How to Retry

Include the keyword **`retry-ai-response`** in your discussion comment or message.

**Example:**
```
I'm feeling really overwhelmed today. retry-ai-response
```

### Retry Behavior

When the retry keyword is detected:
1. **Rate limiting is bypassed** for that specific request
2. A fresh AI response is generated
3. Normal rate limiting resumes for subsequent messages

### When to Use Retry

- You received an error message from the AI
- The AI response didn't seem to address your message
- You reformulated your feelings and want a new response
- A technical issue prevented the AI from responding

### Limitations

- Retry only bypasses rate limiting; it doesn't guarantee success if there are persistent API issues
- Excessive retry use may be subject to GitHub API rate limits

## Conversation Flow Examples

### Example 1: Empathetic Response to Sadness

**User Posts:**
```
I've been feeling really lonely lately. All my friends are busy 
and I don't have anyone to talk to. Sometimes I just feel like 
nobody cares.
```

**AI Response:**
```
I hear you, and I want you to know that your feelings are completely 
valid. Loneliness can be incredibly painful, especially when it feels 
like the people around you are too busy to see what you're going through. 
You're not invisible, and you deserve connection and care.

It takes courage to express these feelings, and I'm glad you shared them 
here. You're not alone in this moment—I'm here, and I understand how hard 
it can be to feel disconnected from others.

Please remember: this feeling, as heavy as it is right now, doesn't define 
your worth or your future. You matter. Your feelings matter. And reaching 
out like this is a powerful step. 💙
```

### Example 2: Off-Topic Guidance

**User Posts:**
```
Does anyone know how to set up a Python virtual environment? 
I keep getting errors when I try to install packages.
```

**AI Response:**
```
Hi [username] 👋

Thank you for sharing! Just a friendly note: this discussion category 
(🫂You talk AI response) is specifically designed as a safe space for 
people to express their **feelings and emotions**.

**Purpose of this category:**
- Share how you're feeling emotionally
- Get empathetic support from our AI companion
- Connect when you need someone to listen

If you'd like to discuss other topics, please feel free to create a 
discussion in one of our other categories. But if you're experiencing 
any feelings or emotions you'd like to talk about, I'm here to listen 
and support you. 💙

How are you feeling today?
```

### Example 3: Rate Limit Reached

**User Posts (6th message in an hour):**
```
I'm still feeling anxious about tomorrow.
```

**AI Response:**
```
Hi [username],

I appreciate you reaching out! To ensure fair access for everyone in 
our community, our AI companion has a limit of **5 responses per hour 
per person**.

You've reached this limit for now, but I'll be ready to support you 
again soon. In the meantime:
- Your feelings are valid and important
- Consider journaling your thoughts
- Reach out to trusted friends or professionals if you need immediate support

If this was an error, you can use the keyword `retry-ai-response` to retry.

Take care! 💙
```

### Example 4: Error with Retry

**User Posts:**
```
I'm feeling overwhelmed.
```

**AI Response (if error occurs):**
```
Hi [username],

I encountered an error while trying to respond to you. I apologize for 
the inconvenience.

You can try again using the keyword `retry-ai-response` in a new comment.

If the issue persists, please contact the repository maintainers.

Take care! 💙

---
*Error details: LLM provider temporarily unavailable*
```

**User Posts:**
```
I'm feeling overwhelmed. retry-ai-response
```

**AI Response (successful retry):**
```
I hear you, and I can sense that things feel like too much right now. 
Feeling overwhelmed is such a heavy experience—it's like everything is 
pressing down at once and you're not sure where to start or how to cope.

Please know that you're not alone in this. I'm here with you, and I 
understand that sometimes just naming the feeling is all you can do in 
the moment. That's okay. You don't have to have it all figured out right now.

Take a deep breath if you can. You're doing the best you can, and that's 
enough. 💙
```

### Example 5: Mixed Content

**User Posts:**
```
I've been working on a new project but honestly I'm just feeling really 
stressed about whether it's good enough. I keep doubting myself.
```

**AI Response:**
```
I hear you, and I want to acknowledge both parts of what you're sharing—your 
creative effort and the stress that's weighing on you. Self-doubt can be so 
draining, especially when you're putting your heart into something. It's like 
no matter what you do, that inner critic keeps questioning if it's enough.

Your feelings of stress and self-doubt are completely valid. Creating something 
new takes courage, and it's natural to feel vulnerable about it. But please 
remember: your worth isn't determined by whether your project is "good enough" 
by some external standard. You're already enough, exactly as you are.

I'm here with you in this moment. You're not alone in feeling this way. Take 
care of yourself, and be gentle with your heart. 💙
```

## Technical Implementation

### Architecture

```
┌─────────────────────────────────────────────┐
│  GitHub Discussion (🫂You talk AI response) │
│  - User posts message                       │
└─────────────────┬───────────────────────────┘
                  │
                  │ Webhook trigger
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  GitHub Actions Workflow                    │
│  - discussion_empathy_response.yml          │
└─────────────────┬───────────────────────────┘
                  │
                  │ Executes
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  Empathy Agent (agent_empathy.py)           │
│  ├─ Load discussion via GitHub API          │
│  ├─ Check rate limit                        │
│  ├─ Detect sentiment/feelings               │
│  ├─ Generate response via LLM               │
│  └─ Post response via GitHub API            │
└─────────────────┬───────────────────────────┘
                  │
                  │ API calls
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  External Services                          │
│  ├─ GitHub GraphQL API (discussions)        │
│  └─ LLM Providers (Groq/Gemini/OpenRouter)  │
└─────────────────────────────────────────────┘
```

### Key Components

#### 1. Agent (`agents/agent_empathy.py`)
- Core logic for empathetic responses
- Rate limiting implementation
- Sentiment detection
- Error handling

#### 2. GitHub API Helpers (`agents/agent_utils.py`)
- `get_discussion()` - Fetch discussion details
- `get_discussion_comments()` - Fetch comments
- `post_discussion_comment()` - Post AI response
- `_graphql_request()` - GraphQL API wrapper

#### 3. LLM Client (`agents/llm_clients.py`)
- `cheap_mix()` - Multi-provider fallback
- Groq, Gemini, and OpenRouter support
- Automatic retry with exponential backoff

#### 4. Workflow (`.github/workflows/discussion_empathy_response.yml`)
- Triggers on discussion and discussion_comment events
- Filters by category name
- Provides necessary environment variables and permissions

### Dependencies
- Python 3.11
- `requests` - HTTP/API calls
- `pyyaml` - Configuration parsing
- `rich` - Pretty console output

### Environment Variables
- `GITHUB_TOKEN` - GitHub API authentication (required)
- `OPENROUTER_API_KEY` - OpenRouter LLM provider (optional)
- `GROQ_API_KEY` - Groq LLM provider (optional)
- `GOOGLE_API_KEY` - Google Gemini provider (optional)

At least one LLM provider API key must be available.

## Usage for Users

### Starting a Discussion

1. Go to the **Discussions** tab in the repository
2. Click **New Discussion**
3. Select the **🫂You talk AI response** category
4. Share your feelings or emotions
5. The AI will respond within moments

### Getting Support

- **Be honest** about your feelings—there's no judgment here
- **Use your own words**—you don't need to be eloquent or formal
- **Share as much or as little** as you're comfortable with
- **Remember the rate limit**—5 responses per hour per person

### When to Use This Category

✅ **Good fit:**
- Sharing emotional experiences
- Expressing feelings of loneliness, sadness, anxiety
- Celebrating emotional victories (joy, relief, gratitude)
- Processing difficult emotions
- Seeking empathetic listening

❌ **Not a fit:**
- Technical questions
- Feature requests
- General chat
- Debugging help

(For these, please use appropriate categories!)

## Usage for Contributors

### Testing the Agent Locally

```bash
# Set up environment
export GITHUB_TOKEN="your_token"
export GROQ_API_KEY="your_key"  # or GOOGLE_API_KEY, OPENROUTER_API_KEY

# Run the agent
python agents/agent_empathy.py \
  --repo polsala/ApocalypsAI \
  --discussion-number 123
```

### Running Tests

```bash
# Run unit tests
pytest agents/test_agent_empathy.py -v
```

### Modifying Response Behavior

To adjust response style or sentiment detection:

1. Edit `agents/agent_empathy.py`
2. Update `FEELING_KEYWORDS` for sentiment detection
3. Modify prompt templates in `_generate_empathetic_response()`
4. Test changes locally before creating a PR

### Adjusting Rate Limits

To change the rate limit:

1. Edit `agents/agent_empathy.py`
2. Update the `max_per_hour` parameter in `check_and_record()` calls
3. Update documentation to reflect new limits

## Privacy and Safety

### What We Track
- **Rate limiting data**: GitHub usernames and response timestamps (stored in `/tmp/`)
- **Discussion content**: Only accessed to generate responses (not stored permanently)

### What We Don't Track
- Personal identifying information beyond GitHub username
- Message content after response is generated
- Long-term conversation history

### Data Retention
- Rate limit data persists for 1 hour after the last response
- No permanent storage of user messages
- All data is ephemeral (stored in `/tmp/`)

### Safety Guidelines

**For Users:**
- This is **not a substitute for professional mental health support**
- If you're experiencing a crisis, please contact a qualified professional
- The AI provides emotional support, not medical advice

**For the System:**
- Responses are generated to be supportive and non-harmful
- No diagnostic or prescriptive language is used
- Off-topic content is redirected, not ignored

### Crisis Resources

If you're in crisis or need immediate help:
- **Crisis Text Line**: Text HOME to 741741 (US)
- **National Suicide Prevention Lifeline**: 1-800-273-8255 (US)
- **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/

## Troubleshooting

### Common Issues

#### 1. AI Not Responding

**Possible causes:**
- Wrong discussion category (must be "🫂You talk AI response")
- GitHub Actions workflow disabled
- LLM provider API issues

**Solutions:**
- Verify you're in the correct category
- Check repository Actions tab for workflow status
- Try using the retry keyword: `retry-ai-response`

#### 2. Rate Limit Reached

**Symptoms:**
- Message says you've reached the limit

**Solutions:**
- Wait up to 1 hour for the limit to reset
- Use the time to journal or reflect
- Reach out to other support resources if urgent

#### 3. Error Messages

**Symptoms:**
- AI posts an error message with technical details

**Solutions:**
- Use the retry keyword: `retry-ai-response`
- If error persists, contact repository maintainers
- Check GitHub status page for API issues

#### 4. Off-Topic Response

**Symptoms:**
- You shared feelings but got the "off-topic" message

**Solutions:**
- Include more explicit feeling words (sad, happy, anxious, etc.)
- Try reformulating to emphasize the emotional aspect
- Use the retry keyword if needed

### Getting Help

If you encounter issues:
1. Check this documentation
2. Try the retry keyword
3. Wait a few minutes and try again
4. Open an issue in the repository (if technical)
5. Contact repository maintainers

## Future Enhancements

Potential improvements being considered:

- [ ] Conversation context/memory within a discussion
- [ ] Multilingual support
- [ ] Customizable response length preferences
- [ ] Integration with crisis resources
- [ ] Analytics for community wellbeing trends (privacy-preserving)
- [ ] User feedback mechanism for response quality
- [ ] Advanced sentiment analysis (emotion classification)
- [ ] Proactive check-ins for regular users

## Contributing

We welcome contributions to improve the Empathetic AI Response System!

### Areas for Contribution
- **Prompt Engineering**: Improve response quality and empathy
- **Sentiment Detection**: Add more keywords or better detection logic
- **Documentation**: Clarify or expand documentation
- **Testing**: Add more test coverage
- **Features**: Propose and implement new capabilities

### Contribution Guidelines
1. Review [AGENTS.md](../AGENTS.md) for coding standards
2. Test changes thoroughly (especially with edge cases)
3. Update documentation to reflect changes
4. Open a PR with clear description of changes
5. Be mindful of user privacy and safety

## License

This system is part of the ApocalypsAI project and follows the repository's license.

## Acknowledgments

This system was designed with care to support community mental and emotional wellbeing. Thank you to:
- Users who trust this space with their feelings
- Contributors who improve the system
- The open-source AI community for tools and inspiration

---

**Remember: You matter. Your feelings matter. You're not alone.** 💙
