# Nightly Resource Allocator

An interactive web dashboard designed to help communities in the post-apocalyptic wasteland whimsically allocate scarce resources among their survivors. Input your available resources and the number of mouths to feed, and let the Allocator suggest a distribution, gauge morale, and even predict your next scavenging success chance!

## Features

*   **Resource Input**: Easily enter quantities for Food, Water, and Medical Supplies.
*   **Survivor Count**: Specify the number of survivors in your group.
*   **Whimsical Allocation Logic**: Provides a suggested distribution based on simple, yet critical, survival needs.
*   **Morale Meter**: A visual indicator of your community's current morale, influenced by resource availability.
*   **Scavenging Success Chance**: A playful prediction of your likelihood to find more resources, tied to current morale.
*   **Interactive UI**: Built with React for a dynamic and engaging user experience.

## How to Run

This utility is a standard React application. Follow these steps to get it running locally:

1.  **Navigate to the utility directory**:
    ```bash
    cd react-webpage/nightly-resource-allocator
    ```

2.  **Install dependencies**:
    ```bash
    npm install
    # or yarn install
    ```

3.  **Start the development server**:
    ```bash
    npm start
    # or yarn start
    ```
    This will open the application in your default web browser, usually at `http://localhost:3000`.

4.  **Build for production (optional)**:
    ```bash
    npm run build
    # or yarn build
    ```
    This creates a `build` directory with optimized static files for deployment.

## Usage

1.  Open the application in your web browser.
2.  Enter the available quantities of "Food Rations", "Water Units", and "Medical Kits".
3.  Enter the "Number of Survivors".
4.  Click the "Calculate Allocation" button.
5.  Observe the suggested resource allocation, the community's morale, and the predicted scavenging success chance.

May your rations be plentiful and your spirits high!
