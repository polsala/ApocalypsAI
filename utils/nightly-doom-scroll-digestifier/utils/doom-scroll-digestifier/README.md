# Doom Scroll Digestifier

## Overview
Feeling overwhelmed by the constant stream of negative news? The Doom Scroll Digestifier is here to help! This whimsical Python CLI utility fetches content from a given URL, identifies sentences laden with 'doom and gloom' keywords, and presents them in a concise digest, always concluding with a touch of ironic optimism or dark humor. It's your daily dose of reality, gently seasoned with a pinch of the absurd.

## Features
- Fetches content from any provided URL.
- Identifies key 'doom' phrases and sentences.
- Summarizes findings into a digestible format.
- Adds a whimsical, ironically positive spin to lighten the mood.

## How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/doom-scroll-digestifier
    ```

2.  **Run the digestifier with a URL:**
    ```bash
    python src/digestifier.py --url "https://example.com/news-article"
    ```

    Replace `"https://example.com/news-article"` with the actual URL you want to digest.

## Example Output

```
--- Doom Scroll Digest --- 

Detected signals of impending doom:
- "Experts warn of an unprecedented global crisis." 
- "The economic collapse is accelerating faster than anticipated." 
- "A new environmental threat looms over the horizon." 

Remember, every cloud has a silver lining, even if it's radioactive. Stay vigilant, but don't forget to hydrate!
```
