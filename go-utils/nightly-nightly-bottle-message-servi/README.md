Nightly Bottle Message Service
--------------------------------
Overview:
A whimsical local network "message in a bottle" service. Clients POST a short text to /bottle and the service keeps it in memory for a configurable retention period. GET /bottle returns all messages still within the retention window.

Build:
    go build -o bottle ./src

Run:
    ./bottle -port 8080 -retention 15

Flags:
    -port int        Port to listen on (default 8080)
    -retention int   Retention time in minutes for stored messages (default 10)

Endpoints:
    POST /bottle
        Body: {"msg":"your message"}
        Stores the message.

    GET /bottle
        Returns JSON array of stored messages:
        [{"msg":"...","timestamp":"2023-01-02T15:04:05Z"}]
