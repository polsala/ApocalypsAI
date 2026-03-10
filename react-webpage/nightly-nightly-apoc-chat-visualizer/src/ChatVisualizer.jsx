import React, { useState, useEffect } from 'react';

const EMOJI_MAP = {
  Alice: '👩‍🚀',
  Bob: '👨‍💻',
  System: '🤖',
  default: '💬'
};

function TypingIndicator({ user }) {
  const emoji = EMOJI_MAP[user] || EMOJI_MAP.default;
  return (
    <div className="flex items-center space-x-2 my-2">
      <span>{emoji}</span>
      <span className="font-mono">{user} is typing</span>
      <div className="flex space-x-1">
        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce"></div>
        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce delay-75"></div>
        <div className="w-2 h-2 bg-green-400 rounded-full animate-bounce delay-150"></div>
      </div>
    </div>
  );
}

function MessageLine({ user, text }) {
  const emoji = EMOJI_MAP[user] || EMOJI_MAP.default;
  return (
    <div className="my-2">
      <span className="font-bold text-yellow-300">{emoji} {user}:</span> <span className="font-mono">{text}</span>
    </div>
  );
}

export default function ChatVisualizer({ messages }) {
  const [displayedMessages, setDisplayedMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      if (index < messages.length) {
        setIsTyping(true);
        setTimeout(() => {
          setIsTyping(false);
          setDisplayedMessages(prev => [...prev, messages[index]]);
          index++;
        }, 800);
      } else {
        clearInterval(interval);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [messages]);

  return (
    <div className="font-mono text-sm">
      {displayedMessages.map((msg, i) => (
        <MessageLine key={i} user={msg.user} text={msg.text} />
      ))}
      {isTyping && <TypingIndicator user={messages[displayedMessages.length]?.user || 'System'} />}
    </div>
  );
}
