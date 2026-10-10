FROM alpine:3.18\nRUN apk add --no-cache tzdata\nCOPY src/emoji_clock.sh /usr/local/bin/emoji_clock.sh\nRUN chmod +x /usr/local/bin/emoji_clock.sh\nENTRYPOINT [\"/usr/local/bin/emoji_clock.sh\"]
