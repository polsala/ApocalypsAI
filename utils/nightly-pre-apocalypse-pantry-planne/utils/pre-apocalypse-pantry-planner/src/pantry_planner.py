import math

def calculate_supplies(num_people: int, duration_days: int) -> dict:
    """
    Calculates essential supplies based on number of people and duration.

    Args:
        num_people (int): The number of people to plan for.
        duration_days (int): The number of days to be self-sufficient.

    Returns:
        dict: A dictionary of required supplies and their quantities.
    """
    if num_people <= 0 or duration_days <= 0:
        raise ValueError("Number of people and duration must be positive integers.")

    # Default consumption rates per person per day
    # These are estimates and can be adjusted.
    daily_consumption = {
        "Water": {"unit": "gallons", "qty_per_person_per_day": 1.0},
        "Canned Food (meals)": {"unit": "cans", "qty_per_person_per_day": 3.0},
        "Batteries (AA)": {"unit": "", "qty_per_person_per_day": 4.0/7}, # 4 per person per week
    }

    supplies = {}

    # Calculate daily/duration-based items
    for item, details in daily_consumption.items():
        required_qty = num_people * duration_days * details["qty_per_person_per_day"]
        if item == "Batteries (AA)":
            required_qty = math.ceil(required_qty) # Round up batteries
        
        supplies[item] = f"{required_qty:.1f}" if details["unit"] else f"{required_qty:.0f}"
        if details["unit"] and required_qty > 0:
            supplies[item] += f" {details['unit']}"

    # Calculate fixed/per-group items
    # First Aid Kits: 1 per 2 people, rounded up
    supplies["First Aid Kits"] = f"{math.ceil(num_people / 2):.0f}"

    # Flashlights: 1 per person, total
    supplies["Flashlights"] = f"{num_people:.0f}"

    return supplies

def main():
    print("Welcome to the Pre-Apocalypse Pantry Planner!\n")

    while True:
        try:
            num_people_str = input("Enter the number of people: ")
            num_people = int(num_people_str)
            if num_people <= 0:
                print("Please enter a positive number for people.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    while True:
        try:
            duration_days_str = input("Enter the duration in days: ")
            duration_days = int(duration_days_str)
            if duration_days <= 0:
                print("Please enter a positive number for duration.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    try:
        shopping_list = calculate_supplies(num_people, duration_days)

        print("\n--- Your Apocalypse Shopping List ---")
        for item, qty in shopping_list.items():
            print(f"{item}: {qty}")
        print("------------------------------------")
        print("Stay safe out there!")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
