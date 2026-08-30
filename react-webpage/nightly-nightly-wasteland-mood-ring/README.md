# Nightly Wasteland Mood Ring

## Summary

The `nightly-wasteland-mood-ring` is a whimsical, interactive React web application designed to help survivors gauge the current 'mood' of the post-apocalyptic wasteland. By inputting various environmental and situational factors, the application calculates a 'mood score' and displays it as a color-coded ring with a corresponding, often humorous, message.

## How to Run

1.  **Navigate to the utility directory:**
    ```bash
    cd react-webpage/nightly-wasteland-mood-ring
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Start the development server:**
    ```bash
    npm start
    ```
    This will typically open the application in your default web browser at `http://localhost:3000`.

## How it Works

The application takes several user inputs related to the wasteland environment:
*   **Scavenger Haul Quality:** How good was your last haul?
*   **Recent Mutant Encounters:** How many unsettling encounters have you had?
*   **Sky Condition:** What does the sky look like today?
*   **Water Supply:** How are your precious water reserves holding up?

Based on these inputs, a simple scoring mechanism determines the overall 'mood' of the wasteland. This mood is then translated into a distinct color (green for hopeful, yellow for cautious, red for perilous) and a unique, often quirky, message providing a snapshot of the day's vibe.

## Example Usage

Once the application is running, you will see a form with several dropdowns. Select your current conditions and observe the 'Wasteland Mood Ring' change color and display a new message. For instance:

*   **Inputs:** Bountiful Scavenger Haul, No Mutant Encounters, Clear Sky, Abundant Water
*   **Output:** A vibrant green ring with a message like: "The irradiated daisies are blooming! A good day to forage. The void seems... less void-y."

*   **Inputs:** Poor Scavenger Haul, Many Mutant Encounters, Ominous Green Glow, Scarce Water
*   **Output:** A deep red ring with a message like: "The void whispers your name, and it sounds hungry. Perhaps a good day to stay in the bunker. Don't forget your lucky lead-lined hat."

This utility is intended for lighthearted situational awareness and morale boosting in dire times.
