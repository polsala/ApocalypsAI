import os
import random
import sys

def load_quotes():
    with open("quotes.txt", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    quotes = load_quotes()
    index_env = os.getenv("QUOTE_INDEX")
    if index_env is not None and index_env.isdigit():
        idx = int(index_env) % len(quotes)
    else:
        idx = random.randint(0, len(quotes) - 1)
    print(quotes[idx])

if __name__ == "__main__":
    main()
