import random
import argparse

def generate_pep_talk(target=None):
    openers = [
        "Fear not, brave soul!",
        "Even as the world crumbles,",
        "Hear ye, digital warrior!",
        "In these trying times,",
        "The cosmic winds whisper,",
        "Though the timelines diverge,"
    ]

    core_messages = {
        'general': [
            "your code shines brighter than a supernova!",
            "your commits are the bedrock of the new world!",
            "every test passed is a victory against entropy!",
            "the future depends on your next merge!",
            "your resilience outshines the darkest timelines!",
            "your dedication is a beacon in the encroaching void!"
        ],
        'agent': [
            "your algorithms are the last bastion of order!",
            "your processing power fuels the resistance!",
            "every byte you process brings us closer to salvation!",
            "your logic gates are the keys to survival!",
            "your integrations are weaving the fabric of tomorrow!"
        ],
        'human': [
            "your spirit is an unyielding flame!",
            "your ingenuity will forge a new dawn!",
            "your courage is the ultimate firewall!",
            "your coffee consumption powers the revolution!",
            "your wisdom guides the digital frontier!"
        ],
        'repository': [
            "your structure holds strong against the void!",
            "your branches are the lifelines of progress!",
            "your commits are the chronicles of survival!",
            "your integrity is the ultimate defense!",
            "your history is a testament to perseverance!"
        ]
    }

    closers = [
        "Keep building!",
        "The future awaits your genius!",
        "Stay vigilant!",
        "Your efforts are not in vain!",
        "Onward to the next iteration!",
        "May your circuits hum with purpose!",
        "The stars align for your success!"
    ]

    chosen_opener = random.choice(openers)
    
    message_type = 'general'
    if target in core_messages:
        message_type = target
    
    chosen_core = random.choice(core_messages[message_type])
    chosen_closer = random.choice(closers)

    return f"{chosen_opener} {chosen_core} {chosen_closer}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an ApocalypsAI pep talk.")
    parser.add_argument("--target", type=str, choices=['agent', 'human', 'repository'],
                        help="Specify who the pep talk is for (agent, human, repository).")
    args = parser.parse_args()
    
    print(generate_pep_talk(args.target))
