import json
import time
import os

# In a real-world scenario, this would use platform-specific libraries
# (e.g., pygetwindow, AppKit, xlib) to get the actual active window title.
# For this self-contained utility and deterministic testing, we simulate it.
# Mock rationale: Avoids platform-specific dependencies and allows for deterministic testing.
# In a real application, this function would be replaced with actual OS calls.
def get_active_window_title_mock(simulated_titles=None, current_index=0):
    if simulated_titles is None or not simulated_titles:
        return "" # Default to empty if no simulation provided or list is empty
    return simulated_titles[current_index % len(simulated_titles)]

def load_config(config_path='src/config.json'):
    # Mock rationale: Allows tests to provide a mock config file path or content.
    # In a real application, this would load from a fixed path, creating a default if missing.
    if not os.path.exists(config_path):
        # Provide a default config if none exists, useful for first run
        default_config = {
            "distraction_keywords": [
                "reddit", "twitter", "facebook", "youtube", "game", "chatgpt"
            ],
            "reminder_message": "Sentinel detected distraction! Time to refocus or take a mindful break.",
            "check_interval_seconds": 5
        }
        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        print(f"Created default config at {config_path}")
        return default_config
    with open(config_path, 'r') as f:
        return json.load(f)

def run_sentinel(simulated_titles=None, max_iterations=None, config_path='src/config.json'):
    config = load_config(config_path)
    distraction_keywords = [k.lower() for k in config.get("distraction_keywords", [])]
    reminder_message = config.get("reminder_message", "Sentinel detected distraction! Time to refocus or take a mindful break.")
    check_interval = config.get("check_interval_seconds", 5)

    print(f"\nFocus Sentinel activated! Monitoring for distractions every {check_interval} seconds...")
    print(f"Distraction keywords: {', '.join(distraction_keywords)}")
    print("Press Ctrl+C to stop.\n")

    iteration = 0
    while True:
        if max_iterations is not None and iteration >= max_iterations:
            break

        current_title = get_active_window_title_mock(simulated_titles, iteration)
        current_title_lower = current_title.lower()

        is_distracting = False
        for keyword in distraction_keywords:
            if keyword in current_title_lower:
                is_distracting = True
                break

        if is_distracting:
            print(f"[{time.strftime('%H:%M:%S')}] {reminder_message} (Detected: '{current_title}')")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] All clear. Current focus: '{current_title}'")

        iteration += 1
        time.sleep(check_interval)

if __name__ == "__main__":
    try:
        run_sentinel()
    except KeyboardInterrupt:
        print("\nFocus Sentinel deactivated. Stay focused!")
