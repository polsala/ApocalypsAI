## Nightly Cosmic Compass

This utility provides a whimsical, interactive web interface that visualizes your current geographical location on a stylized cosmic map. It overlays this with hypothetical celestial bodies and imagined alien civilizations, offering a playful perspective on our place in the universe.

### Philosophy

Inspired by the "Anarchy with discipline" philosophy of ApocalypsAI, this tool is self-contained, testable, and aims to be both fun and a gentle reminder of the vastness beyond our immediate surroundings.

### Technology Stack

*   **Frontend**: React, Vite, Tailwind CSS
*   **Mapping**: Leaflet.js (for basic geo-positioning)
*   **Mocking**: Jest (for unit and integration tests)

### Features

*   **Real-time Location Display**: Uses browser geolocation to pinpoint your current position.
*   **Cosmic Map Overlay**: A stylized, non-realistic map that blends geographical features with celestial elements.
*   **Hypothetical Celestial Bodies**: Randomly generated planets, nebulae, and asteroid fields.
*   **Imagined Alien Civilizations**: Fictional markers representing potential alien settlements, with whimsical names and descriptions.
*   **Interactive Elements**: Hovering over celestial bodies or civilizations reveals fun facts or lore.

### Setup and Usage

1.  **Prerequisites**: Node.js and npm/yarn installed.
2.  **Installation**: 
    ```bash
    git clone <repository_url>
    cd polsala/ApocalypsAI
    cd react-webpage/nightly-cosmic-compass
    npm install
    ```
3.  **Development Server**: 
    ```bash
    npm run dev
    ```
    This will start a local development server. Open your browser to the provided URL (usually `http://localhost:5173`).
4.  **Build for Production**: 
    ```bash
    npm run build
    ```
    This will create a production-ready build in the `dist` folder.

### Testing

To run the tests:

```bash
npm test
```

### Contributing

Contributions are welcome! Please follow the standard ApocalypsAI contribution guidelines.
