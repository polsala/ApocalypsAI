FROM golang:1.22-alpine

WORKDIR /app

# Copy go.mod and go.sum first to leverage Docker cache
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the application source code
COPY . .

# Build the Go application
RUN go build -o temporal-replay-box src/main.go

# Expose the port the application listens on
EXPOSE 8080

# Command to run the application
CMD ["./temporal-replay-box"]
