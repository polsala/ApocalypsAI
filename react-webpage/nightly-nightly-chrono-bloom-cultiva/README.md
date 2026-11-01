# Nightly Chrono-Bloom Cultivator

## Summary
An interactive web interface to cultivate digital 'chrono-blooms' that visually track time, tasks, or moments of peace, blooming over a set duration. Each bloom represents a period of focus, a goal, or simply a moment to appreciate, growing from a bud to a full flower as time progresses.

## Whimsical Utility
In the post-apocalyptic landscape, time can feel distorted or meaningless. The Chrono-Bloom Cultivator offers a whimsical way to reclaim and visualize time, fostering a sense of progress and beauty amidst the chaos. Plant a 'bloom' for your next scavenging run, a meditation session, or simply to watch a digital flower grow, reminding you that even in the void, time continues, and beauty can be cultivated.

## How to Run
This is a React application. To run it locally, you'll need Node.js and npm installed.

1.  **Navigate to the utility directory:**
    ```bash
    cd nightly-chrono-bloom-cultivator
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use
1.  **Add a New Bloom:**
    *   Enter a `Bloom Name` (e.g., "Scavenge Sector 7", "Meditate on the Void", "Read Ancient Texts").
    *   Enter a `Duration (minutes)` for how long the bloom should take to fully grow.
    *   Click the "Plant Bloom" button.
2.  **Watch it Grow:**
    *   Each planted bloom will appear as a card, starting as a small bud.
    *   As time passes, the bloom will visually grow, changing color and size, until it reaches full bloom.
    *   A progress bar indicates how much time has elapsed.
3.  **Delete a Bloom:**
    *   Click the "Wither" button on any bloom card to remove it.

## Project Structure
```
nightly-chrono-bloom-cultivator/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── App.css             # Styling for the main application
│   ├── App.js              # Main React component
│   ├── ChronoBloom.js      # Component for a single chrono-bloom
│   └── index.js            # React application entry point
├── tests/
│   └── App.test.js         # Jest/React Testing Library tests
├── package.json            # Project dependencies and scripts
└── README.md
```

## Automated Tests
To run the tests, use the following command:
```bash
npm test
```
This will execute the tests using Jest and React Testing Library.
