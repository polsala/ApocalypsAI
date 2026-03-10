# nightly-apoc-chat-visualizer

A whimsical React component that visualizes chat logs in a retro terminal style with emoji flair and animated typing indicators.

## Features

- Terminal-style chat rendering
- Animated typing indicators
- Emoji-enhanced messages
- Fully responsive design

## Usage

```jsx
import ChatVisualizer from './src/ChatVisualizer';

const messages = [
  { user: 'Alice', text: 'Hello there!' },
  { user: 'Bob', text: 'General Kenobi!' },
];

function App() {
  return <ChatVisualizer messages={messages} />;
}
```

## Development

Install dependencies:

```
npm install
```

Run development server:

```
npm start
```

Build for production:

```
npm run build
```

## Testing

Tests are written with Jest and React Testing Library:

```
npm test
```
