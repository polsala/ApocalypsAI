## Nightly Cosmic Compass

This utility provides a whimsical web interface that displays your current geographical location overlaid on a stylized celestial map. It also offers 'cosmic advice' based on your location, adding a touch of playful mystique to your day.

### Features

*   **Interactive Celestial Map**: Visualize your location on a beautifully rendered, fictional star chart.
*   **Location-Based Cosmic Advice**: Receive unique, lighthearted advice tailored to your current position.
*   **Responsive Design**: Works on various screen sizes.

### Setup

1.  **Prerequisites**: Node.js and npm (or yarn) installed.
2.  **Clone the repository**: `git clone https://github.com/polsala/ApocalypsAI.git`
3.  **Navigate to the utility directory**: `cd ApocalypsAI/react-webpage/nightly-cosmic-compass`
4.  **Install dependencies**: `npm install` (or `yarn install`)
5.  **Start the development server**: `npm start` (or `yarn start`)

This will launch the application in your browser, typically at `http://localhost:3000`.

### Usage

Upon loading, the application will attempt to detect your current location using the browser's Geolocation API. If permission is granted, your location will be marked on the celestial map, and a piece of cosmic advice will be displayed. You can manually refresh the advice by clicking the 'Seek New Wisdom' button.

### Testing

To run the included tests, execute:

`npm test` (or `yarn test`)

### Contributing

Contributions are welcome! Please refer to the main ApocalypsAI repository for contribution guidelines.
