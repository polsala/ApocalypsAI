## Cosmic Comm Relay

Welcome, intrepid interstellar communicator! The Cosmic Comm Relay is a whimsical web application that allows you to send and receive short, encrypted messages across simulated cosmic distances. Think of it as a cosmic postcard system, powered by a dash of imagination and a sprinkle of modern web tech.

### How it Works

1.  **Sending a Whisper:**
    *   Enter your message (up to 100 characters).
    *   Choose a destination planet (from a predefined list).
    *   Click "Send Whisper". Your message will be encoded and a simulated travel time will be displayed.

2.  **Receiving Whispers:**
    *   Your incoming whispers will appear in the "Incoming Whispers" section.
    *   Each whisper will show its origin, the decoded message, and the time it took to arrive.

### Technology Stack

*   **Frontend:** React
*   **Styling:** Basic CSS for a retro-futuristic feel.
*   **Backend (Simulated):** All logic is client-side for simplicity. Message encoding/decoding and simulated travel times are handled within the React components.

### Setup and Running

1.  **Prerequisites:** Node.js and npm (or yarn) installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
3.  **Navigate to the utility:**
    ```bash
    cd utils/nightly-cosmic-comm-relay
    ```
4.  **Install dependencies:**
    ```bash
    npm install
    ```
5.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the application in your browser, usually at `http://localhost:3000`.

### Development Notes

*   The "cosmic distance" and "travel time" are purely simulated. They are based on a simple random number generator and a predefined list of planets.
*   Message encoding uses a basic Caesar cipher for a touch of retro-futurism. It's not cryptographically secure!
*   The goal is to provide a fun, interactive experience rather than a robust communication tool.

### Testing

Run the tests using:

```bash
npm test
```

This will execute the unit tests for the core encoding/decoding logic and component rendering.
