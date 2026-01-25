Nightly Docker Quote Server

A whimsical Dockerized HTTP server that serves a random apocalyptic quote on each request.

Build:
 docker build -t nightly-quote-server .

Run:
 docker run -p 8080:8080 nightly-quote-server

Access the server at http://localhost:8080/ . Each request returns a different quote from a curated list.

Test:
 Run the Go tests locally (requires Go 1.22+):
 go test ./...

The tests verify that the server returns a quote from the known list.
