## Docker Wasteland Weeder

A containerized utility that identifies and removes unused Docker resources while whispering encouraging gardening metaphors. Perfect for keeping your Docker ecosystem tidy without the existential dread of manual pruning.

### Usage
```bash
# Scan for digital weeds
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock polsala/nightly-docker-wasteland-weeder

# With verbose storytelling
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock polsala/nightly-docker-wasteland-weeder --whisper
```
