# Apocalypse Playlist Generator

A Dockerized service that creates survival-themed playlists mixing music genres with practical apocalypse preparedness tips. Accepts parameters like `--mood=dark` or `--genre=industrial` to customize output.

## Usage
```bash
docker build -t apocalypsys .
docker run -p 5000:5000 apocalypsys
# Visit http://localhost:5000/playlist?genre=post-apocalyptic
```
