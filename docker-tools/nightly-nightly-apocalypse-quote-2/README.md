Apocalypse Quote Service

A tiny Dockerized HTTP service that serves random apocalypse-themed quotes.

Usage

Build the image:
docker build -t apocalypse-quote .

Run the container:
docker run -p 8080:8080 apocalypse-quote

Request a quote:
curl http://localhost:8080/quote

The response will be JSON:
{
  \"quote\": \"When the world ends, the jokes are still funny.\"
}
