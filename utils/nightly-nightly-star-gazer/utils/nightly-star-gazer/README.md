# Nightly Star Gazer

## 🌠 Gaze Upon the Stars of Your Repository! 🌠

The `nightly-star-gazer` is a whimsical utility designed to bring a touch of cosmic wonder to your repository tracking. It fetches the current star count for a given GitHub repository and generates a 'Star-Gazing Report,' assigning a unique constellation name based on the repository's stellar popularity.

### ✨ Features

*   **Real-time Star Count**: Fetches the latest star count directly from GitHub.
*   **Whimsical Constellations**: Assigns a fun, cosmic name to your repository based on its star tier.
*   **Clear Reporting**: Provides a concise and engaging report of your repository's standing in the GitHub galaxy.

### 🚀 Usage

To use the Star Gazer, simply run the `star_gazer.py` script with the `--repo` argument, specifying the `owner/repository_name`.

```bash
python src/star_gazer.py --repo polsala/ApocalypsAI
```

**Example Output:**

```
🌌 Nightly Star-Gazing Report 🌌
For polsala/ApocalypsAI

Repository: polsala/ApocalypsAI
Current Stars: 1234
Constellation: Stellar Swarm

Keep shining bright, cosmic voyager!
```

### 🌟 Constellation Tiers

Your repository's star count determines its celestial designation:

*   **0-99 Stars**: Dust Cloud (Just starting its cosmic journey!)
*   **100-499 Stars**: Nebula Nook (A cozy corner of emerging brilliance!)
*   **500-999 Stars**: Comet Cluster (Gathering speed and attention!)
*   **1000-4999 Stars**: Stellar Swarm (A vibrant collection of admirers!)
*   **5000-9999 Stars**: Galactic Gem (A true treasure in the vast expanse!)
*   **10000+ Stars**: Cosmic Colossus (A monumental force, visible across galaxies!)

### 🛠️ Development

This utility is written in Python 3.11 and uses `requests` for API calls and `rich` for enhanced console output. Ensure these are installed in your environment:

```bash
pip install requests rich
```
