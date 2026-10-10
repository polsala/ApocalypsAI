import sys
import os

MOOD_FILE = '/app/mood.txt'

def get_mood():
    if os.path.exists(MOOD_FILE):
        with open(MOOD_FILE, 'r') as f:
            return f.read().strip()
    return "Content" # Default mood

def set_mood(mood):
    with open(MOOD_FILE, 'w') as f:
        f.write(mood)

def main():
    args = sys.argv[1:]
    current_mood = get_mood()

    if not args:
        print(f"Critter is feeling {current_mood}.")
    else:
        command = args[0].lower()
        if command == 'feed':
            set_mood("Happy")
            print("Critter fed! It's feeling Happy.")
        elif command == 'play':
            set_mood("Excited")
            print("Critter played with! It's feeling Excited.")
        else:
            print(f"Unknown command: '{command}'. Critter is still feeling {current_mood}.")

if __name__ == '__main__':
    main()
