FROM \"golang:1.22-alpine\" AS builder\nWORKDIR /app\nCOPY src/main.go .\nRUN go build -o echo .\n\nFROM alpine\nWORKDIR /app\nCOPY --from=builder /app/echo .\nEXPOSE 8080\nCMD [\"./echo\"]\n
