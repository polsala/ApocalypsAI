FROM alpine:3.20\nWORKDIR /app\nCOPY src/main.sh /app/main.sh\nCOPY src/quotes.txt /app/quotes.txt\nRUN chmod +x /app/main.sh\nENTRYPOINT ["./main.sh"]
