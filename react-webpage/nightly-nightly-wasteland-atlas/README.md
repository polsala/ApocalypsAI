# Nightly Wasteland Atlas

The Nightly Wasteland Atlas is a whimsical-yet-useful interactive web application designed for survivors navigating the post-apocalyptic landscape. It allows users to plot, visualize, and manage critical locations, resources, and hazards on a dynamic, albeit conceptual, map. Keep track of your findings, plan your routes, and share vital intelligence with your fellow survivors (or keep it all to yourself, we don't judge).

## Features

*   **Add New Locations**: Easily mark down new discoveries, whether it's a stash of Nuka-Cola, a safe haven, or a lurking Deathclaw.
*   **Categorize & Filter**: Assign types (Resource, Safe Zone, Hazard) to your locations and filter the map view to see only what's relevant.
*   **Interactive List View**: While not a literal map, the interactive list allows you to quickly browse and manage your plotted points, complete with simulated coordinates.
*   **Persistent Storage**: Your plotted locations are saved locally in your browser, so your intel is safe even after a system reboot (unless the browser cache gets irradiated).

## How to Run

1.  **Prerequisites**: Ensure you have Node.js and npm installed.
2.  **Navigate**: Change directory into `nightly-wasteland-atlas`.
3.  **Install Dependencies**:
    ```bash
    npm install
    ```
4.  **Start the Application**:
    ```bash
    npm start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

## How to Use

Upon launching the Atlas:

1.  **Add a Location**: Use the "Add New Location" form at the top.
    *   **Name**: A descriptive name for your point of interest.
    *   **Type**: Select from "Resource", "Safe Zone", or "Hazard".
    *   **Coordinates**: Enter simulated coordinates (e.g., "X:123 Y:456").
    *   **Description**: Any additional notes about the location.
2.  **View Locations**: All added locations will appear in the list below the form.
3.  **Filter Locations**: Use the "Filter by Type" dropdown to narrow down the displayed locations.
4.  **Clear All**: The "Clear All Locations" button will wipe your local map clean. Use with caution!

## Technologies Used

*   **React**: For building the interactive user interface.
*   **JavaScript (ES6+)**: Core logic and functionality.
*   **HTML/CSS**: Structure and styling.
*   **Local Storage**: For client-side data persistence.

## Development Notes

This utility focuses on core React concepts and local data management, providing a functional "map" experience without external mapping libraries, ensuring it remains lightweight and easily runnable offline.
