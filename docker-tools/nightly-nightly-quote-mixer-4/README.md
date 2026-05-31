Nightly Quote Mixer

A tiny Dockerized HTTP service that returns a whimsical mixed quote on each request.

Usage:
  docker build -t nightly-quote-mixer .
  docker run -p 5000:5000 nightly-quote-mixer

Then request:
  curl http://localhost:5000/quote

Response example:
  {"quote":"..."}

License: MIT
