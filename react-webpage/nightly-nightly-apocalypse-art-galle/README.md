## Nightly Apocalypse Art Gallery

This utility provides a whimsical, interactive web gallery showcasing AI-generated "apocalypse art." Users can filter the art by theme, color palette, and even "apocalypse severity" to discover their favorite post-apocalyptic masterpieces.

### Setup

1.  **Prerequisites**: Ensure you have Node.js and npm (or yarn) installed.
2.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI
    ```
3.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-apocalypse-art-gallery
    ```
4.  **Install dependencies**:
    ```bash
    npm install
    ```

### Running the Application

1.  **Start the development server**:
    ```bash
    npm start
    ```
    This will launch the gallery in your default web browser, usually at `http://localhost:3000`.

### Features

*   **Interactive Art Display**: View a collection of unique AI-generated apocalypse art.
*   **Filtering**: Filter art by:
    *   **Theme**: e.g., "Cosmic Doom", "Mutant Mayhem", "Robo-Rage", "Nature's Revenge".
    *   **Color Palette**: e.g., "Desaturated Grays", "Fiery Reds", "Eerie Greens", "Neon Glow".
    *   **Apocalypse Severity**: A slider from "Mildly Concerning" to "Total Annihilation".
*   **Responsive Design**: Works on various screen sizes.

### How it Works

The application uses React to build the user interface. Art data (including themes, palettes, and severity ratings) is stored in a mock JSON file. The filtering logic is handled client-side, allowing for immediate updates to the displayed art.

### Testing

To run the automated tests:

```bash
npm test
```

This will execute the Jest tests, which verify the filtering and rendering logic using mocked data.
