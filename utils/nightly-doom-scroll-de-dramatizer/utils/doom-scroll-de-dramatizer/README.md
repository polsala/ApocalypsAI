# Doom-Scroll De-Dramatizer

## 📜 Overview

In an age where every headline screams "APOCALYPSE NOW!", the Doom-Scroll De-Dramatizer is your digital balm. This whimsical-yet-useful utility takes overly sensational or alarming text and gently rephrases it, stripping away the hyperbole to present information with a more neutral, resilient, or even cautiously optimistic tone. Perfect for those moments when you need to stay informed without succumbing to the relentless tide of "doom-scrolling."

It won't change the facts, but it will help you process them without the added emotional burden of sensationalist language.

## ✨ Features

*   **Hyperbole Reduction**: Replaces common sensationalist words with more neutral alternatives.
*   **Emotional Tone Adjustment**: Shifts the narrative from panic to perspective.
*   **Resilience Framing**: Adds subtle hints of enduring strength and adaptability.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 How to Use

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/doom-scroll-de-dramatizer
    ```
2.  **Run**: Execute the `dedramatizer.py` script with your text input.

    *   **From a string**:
        ```bash
        python src/dedramatizer.py "Breaking: Catastrophe looms as critical systems fail, plunging the world into chaos and despair!"
        ```
    *   **From a file**:
        ```bash
        echo "Urgent: A new crisis threatens to devastate our fragile society, causing widespread panic and irreversible damage." > input.txt
        python src/dedramatizer.py --file input.txt
        rm input.txt
        ```
    *   **From standard input (pipe)**:
        ```bash
        echo "The economy is collapsing! We face an unprecedented disaster!" | python src/dedramatizer.py
        ```

## 🛠️ How It Works

The `dedramatizer.py` script employs a set of predefined, configurable replacement rules. It iterates through the input text, identifying keywords and phrases associated with sensationalism, and replaces them with calmer, more objective, or resilience-focused alternatives. It's a simple, rule-based system designed for clarity and emotional regulation, not deep linguistic analysis.

## 🧪 Example Output

**Original Input:**
`"Breaking: Catastrophe looms as critical systems fail, plunging the world into chaos and despair! Urgent action is needed to avert total disaster and widespread panic."`

**De-Dramatized Output:**
`"Update: A significant challenge is emerging as key systems encounter issues, leading to a period of disruption and concern. Proactive measures are advisable to navigate the serious situation and manage broad apprehension. Remember, adaptability is key."`
