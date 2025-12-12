## Nightly Cosmic Compass

This whimsical utility, built with Node.js, generates "cosmic coordinates" for celestial navigation. It takes the current time and adds a sprinkle of imaginative flair to produce coordinates that are both fun and vaguely reminiscent of astronomical data.

### Purpose

In a world where the stars might be our only guide, the Cosmic Compass provides a playful way to orient oneself. It's designed to be a lighthearted tool for anyone who enjoys a bit of stargazing or just needs a unique way to mark time.

### Usage

To use the Cosmic Compass, simply run the script:

```bash
node src/main.js
```

The output will be a JSON object containing the generated celestial coordinates.

### How it Works

The utility uses the current date and time to seed a pseudo-random number generator. This generator then produces values for:

*   **Ascension (RA)**: Similar to right ascension, representing a celestial longitude.
*   **Declination (Dec)**: Similar to declination, representing a celestial latitude.
*   **Epoch (E)**: A whimsical time marker, adding a temporal flavor.
*   **Constellation (C)**: A randomly assigned, fantastical constellation name.

### Example Output

```json
{
  "RA": "14h 32m 15.2s",
  "Dec": "+25° 10' 05.5\"",
  "Epoch": "Stardust Era",
  "Constellation": "The Glimmering Quill"
}
```

### Contributing

Feel free to fork this repository and add your own cosmic twists! Contributions are welcome via pull requests.
