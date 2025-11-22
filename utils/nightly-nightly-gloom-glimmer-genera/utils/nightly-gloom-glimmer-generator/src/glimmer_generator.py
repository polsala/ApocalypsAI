import argparse
import os

class GlimmerGenerator:
    def __init__(self):
        # Define a set of simple rules to add a "glimmer"
        # Each rule is a tuple: (negative_phrase, positive_reframe)
        self.rules = [
            ("dwindling supplies", "dwindling supplies, encouraging resourceful new strategies"),
            ("scarce resources", "scarce resources, fostering ingenuity and collaboration"),
            ("another day of rain", "another day of rain, ensuring fresh water collection opportunities"),
            ("broken communication", "broken communication, highlighting the value of local networks"),
            ("isolated", "isolated, yet fostering strong bonds within our immediate community"),
            ("danger lurks", "danger lurks, keeping us vigilant and prepared"),
            ("uncertain future", "an uncertain future, ripe with possibilities for rebuilding"),
            ("lost hope", "lost hope, but finding strength in collective resilience"),
            ("struggle", "struggle, forging stronger spirits and innovative solutions"),
            ("despair", "despair, which we counter with small acts of kindness and shared purpose"),
        ]

    def generate_glimmer(self, text):
        glimmered_text = text
        for negative, positive in self.rules:
            # Case-insensitive replacement for simplicity. Could be extended with regex.
            glimmered_text = glimmered_text.replace(negative, positive)
            glimmered_text = glimmered_text.replace(negative.capitalize(), positive.capitalize())
        return glimmered_text

    def process_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self.generate_glimmer(content)

def main():
    parser = argparse.ArgumentParser(
        description="Transforms gloomy text into glimmering prose, finding hope in the apocalypse."
    )
    parser.add_argument(
        "input_file",
        help="Path to the text file containing the gloomy input."
    )
    args = parser.parse_args()

    generator = GlimmerGenerator()
    try:
        glimmered_output = generator.process_file(args.input_file)
        print(glimmered_output)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=os.stderr)
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=os.stderr)
        exit(1)

if __name__ == "__main__":
    main()
