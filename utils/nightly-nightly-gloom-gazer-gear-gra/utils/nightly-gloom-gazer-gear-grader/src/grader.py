import sys
from typing import List, Dict, Tuple

class GearGrader:
    """
    Grades gear items based on their type and condition score.
    """

    PRIORITY_CRITICAL = "CRITICAL"
    PRIORITY_URGENT = "URGENT"
    PRIORITY_MAINTAIN = "MAINTAIN"
    PRIORITY_GOOD = "GOOD"
    PRIORITY_MISC = "MISC" # For non-essential items with very low condition

    ESSENTIAL_TYPES = {"weapon", "armor", "tool"}

    def grade_item(self, item_name: str, item_type: str, condition_score: int) -> str:
        """
        Determines the priority level for a single gear item.

        Args:
            item_name (str): The name of the item.
            item_type (str): The category of the item (e.g., "weapon", "armor", "tool").
            condition_score (int): The condition of the item, 0-100.

        Returns:
            str: The priority level (e.g., "CRITICAL", "URGENT", "MAINTAIN", "GOOD", "MISC").
        """
        item_type_lower = item_type.lower()

        if item_type_lower not in self.ESSENTIAL_TYPES and condition_score < 20:
            return self.PRIORITY_MISC # Non-essential and very bad condition

        if condition_score < 20:
            return self.PRIORITY_CRITICAL # Very low condition, regardless of type

        if condition_score < 50:
            if item_type_lower in self.ESSENTIAL_TYPES:
                return self.PRIORITY_URGENT # Essential and low condition
            else:
                return self.PRIORITY_MAINTAIN # Non-essential but still usable

        if condition_score < 80:
            return self.PRIORITY_MAINTAIN # Moderate condition

        return self.PRIORITY_GOOD # Good condition

    def process_gear_list(self, gear_lines: List[str]) -> Dict[str, List[Tuple[str, str, int]]]:
        """
        Processes a list of gear item strings and grades them.

        Args:
            gear_lines (List[str]): A list of strings, each in "Item Name,Type,Condition Score" format.

        Returns:
            Dict[str, List[Tuple[str, str, int]]]: A dictionary where keys are priority levels
            and values are lists of (item_name, item_type, condition_score) tuples.
        """
        graded_gear: Dict[str, List[Tuple[str, str, int]]] = {
            self.PRIORITY_CRITICAL: [],
            self.PRIORITY_URGENT: [],
            self.PRIORITY_MAINTAIN: [],
            self.PRIORITY_GOOD: [],
            self.PRIORITY_MISC: [],
        }

        for line in gear_lines:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.split(',')
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed line: '{line}'. Expected 'Name,Type,Condition'.", file=sys.stderr)
                    continue
                item_name = parts[0].strip()
                item_type = parts[1].strip()
                condition_score = int(parts[2].strip())

                if not (0 <= condition_score <= 100):
                    print(f"Warning: Skipping item '{item_name}' with invalid condition score: {condition_score}. Must be 0-100.", file=sys.stderr)
                    continue

                priority = self.grade_item(item_name, item_type, condition_score)
                graded_gear[priority].append((item_name, item_type, condition_score))
            except ValueError:
                print(f"Warning: Skipping malformed line: '{line}'. Condition score must be an integer.", file=sys.stderr)
            except Exception as e:
                print(f"An unexpected error occurred processing line '{line}': {e}", file=sys.stderr)

        return graded_gear

    def format_report(self, graded_gear: Dict[str, List[Tuple[str, str, int]]]) -> str:
        """
        Formats the graded gear into a human-readable report string.
        """
        report_parts = ["--- Gear Grading Report ---"]

        priority_order = [
            (self.PRIORITY_CRITICAL, "Requires immediate attention!"),
            (self.PRIORITY_URGENT, "Needs repair soon"),
            (self.PRIORITY_MAINTAIN, "Keep an eye on it"),
            (self.PRIORITY_GOOD, "Ready for action!"),
            (self.PRIORITY_MISC, "Non-essential, low priority"),
        ]

        for priority, description in priority_order:
            items = graded_gear.get(priority, [])
            if items:
                report_parts.append(f"\n{priority} ({description}):")
                for item_name, item_type, condition_score in items:
                    report_parts.append(f"  - {item_name} ({item_type}) - Condition: {condition_score}/100")

        return "\n".join(report_parts)

def main(argv: List[str] = None):
    """
    Main entry point for the Gear Grader utility.
    Processes a gear list file and prints a grading report.
    """
    if argv is None:
        argv = sys.argv

    if len(argv) < 2:
        print("Usage: python src/grader.py <gear_file.txt>")
        sys.exit(1)

    file_path = argv[1]
    try:
        with open(file_path, 'r') as f:
            gear_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}", file=sys.stderr)
        sys.exit(1)

    grader = GearGrader()
    graded_gear = grader.process_gear_list(gear_lines)
    report = grader.format_report(graded_gear)
    print(report)

if __name__ == "__main__":
    main()
