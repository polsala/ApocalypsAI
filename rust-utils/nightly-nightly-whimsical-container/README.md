# Whimsical Container Namer

CLI tool that generates creative names for containers/services. Example: `docker run --name $(whimsical-namer --theme steampunk)`.

## Usage
```bash
whimsical-namer [OPTIONS]
  --theme <THEME>   # Available: steampunk, cyberpunk, fantasy, corporate, pirate
  --mood <MOOD>     # Available: serious, playful, absurd
  --count <NUM>     # Number of names to generate
```
