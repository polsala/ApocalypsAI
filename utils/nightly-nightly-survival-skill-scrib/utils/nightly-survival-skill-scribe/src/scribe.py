import json
import os
import sys

class SurvivalScribe:
    def __init__(self, data_file="skills.json"):
        self.data_file = data_file
        self.skills = self._load_skills()

    def _load_skills(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Handle empty or malformed JSON file
                return {}
        return {}

    def _save_skills(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.skills, f, indent=4)

    def add_skill(self, name, description):
        name_lower = name.lower()
        if name_lower in self.skills:
            return False, f"Skill '{name}' already exists. Use 'update' to modify."
        self.skills[name_lower] = {"name": name, "description": description}
        self._save_skills()
        return True, f"Skill '{name}' added."

    def update_skill(self, name, description):
        name_lower = name.lower()
        if name_lower not in self.skills:
            return False, f"Skill '{name}' not found. Use 'add' to create it."
        self.skills[name_lower]["description"] = description
        self._save_skills()
        return True, f"Skill '{name}' updated."

    def get_skill(self, name):
        name_lower = name.lower()
        return self.skills.get(name_lower)

    def list_skills(self):
        return sorted([skill_data for skill_data in self.skills.values()], key=lambda x: x['name'])

    def search_skills(self, keyword):
        keyword_lower = keyword.lower()
        results = []
        for skill_data in self.skills.values():
            if keyword_lower in skill_data["name"].lower() or \
               keyword_lower in skill_data["description"].lower():
                results.append(skill_data)
        return sorted(results, key=lambda x: x['name'])

def main():
    scribe = SurvivalScribe(data_file=os.path.join(os.path.dirname(__file__), "skills.json"))
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  python scribe.py add \"Skill Name\" \"Description\"")
        print("  python scribe.py update \"Skill Name\" \"New Description\"")
        print("  python scribe.py get \"Skill Name\"")
        print("  python scribe.py list")
        print("  python scribe.py search \"keyword\"")
        sys.exit(1)

    command = args[0]

    if command == "add" and len(args) == 3:
        success, message = scribe.add_skill(args[1], args[2])
        print(message)
        sys.exit(0 if success else 1)
    elif command == "update" and len(args) == 3:
        success, message = scribe.update_skill(args[1], args[2])
        print(message)
        sys.exit(0 if success else 1)
    elif command == "get" and len(args) == 2:
        skill = scribe.get_skill(args[1])
        if skill:
            print(f"Skill: {skill['name']}\nDescription: {skill['description']}")
        else:
            print(f"Skill '{args[1]}' not found.")
            sys.exit(1)
    elif command == "list" and len(args) == 1:
        skills = scribe.list_skills()
        if skills:
            print("--- All Survival Skills ---")
            for skill in skills:
                print(f"- {skill['name']}: {skill['description']}")
            print("-------------------------")
        else:
            print("No skills recorded yet.")
    elif command == "search" and len(args) == 2:
        results = scribe.search_skills(args[1])
        if results:
            print(f"--- Search Results for '{args[1]}' ---")
            for skill in results:
                print(f"- {skill['name']}: {skill['description']}")
            print("------------------------------------")
        else:
            print(f"No skills found matching '{args[1]}'.")
    else:
        print(f"Unknown command or incorrect arguments for '{command}'.")
        main() # Print usage again
        sys.exit(1)

if __name__ == "__main__":
    main()
