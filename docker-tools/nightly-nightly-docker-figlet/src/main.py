#!/usr/bin/env python3
import argparse
import sys
from pyfiglet import Figlet

def render_text(text: str, font: str = "standard") -> str:
    fig = Figlet(font=font)
    return fig.renderText(text)

def main():
    parser = argparse.ArgumentParser(description="Render text as ASCII art using Figlet.")
    parser.add_argument("text", help="Text to render")
    parser.add_argument("-f", "--font", default="standard", help="Figlet font to use")
    args = parser.parse_args()
    output = render_text(args.text, args.font)
    sys.stdout.write(output)

if __name__ == "__main__":
    main()
