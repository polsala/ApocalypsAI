import time
import argparse
import sys

def chime(message):
    """Prints a themed chime message."""
    print(f"\n🔔 Chronos-Chime: {message} 🔔")

def run_timer(work_duration_min, break_duration_min, cycles):
    """Runs the Pomodoro timer."""
    print(f"Starting Chronos-Chime Task Aligner for {cycles} cycles.")
    print(f"Work: {work_duration_min} min, Break: {break_duration_min} min.")

    try:
        for i in range(cycles):
            chime(f"Cycle {i+1}/{cycles}: Time to FOCUS! ({work_duration_min} min)")
            time.sleep(work_duration_min * 60) # Convert minutes to seconds

            if i < cycles - 1: # Don't break after the last work session
                chime(f"Cycle {i+1}/{cycles}: Time for a RECHARGE! ({break_duration_min} min)")
                time.sleep(break_duration_min * 60)
            else:
                chime(f"Cycle {i+1}/{cycles}: Work session complete!")

        chime("All cycles complete! Excellent alignment!")

    except KeyboardInterrupt:
        chime("Alignment interrupted. Until next time, stay aligned!")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Chronos-Chime Task Aligner: A whimsical Pomodoro timer for focused work."
    )
    parser.add_argument(
        "-w", "--work", type=float, default=25,
        help="Duration of each work session in minutes (default: 25)"
    )
    parser.add_argument(
        "-b", "--break", type=float, default=5,
        help="Duration of each short break in minutes (default: 5)"
    )
    parser.add_argument(
        "-c", "--cycles", type=int, default=4,
        help="Number of work-break cycles (default: 4)"
    )
    args = parser.parse_args()

    if args.work <= 0 or args.break < 0 or args.cycles <= 0: # Break can be 0
        print("Error: Work duration and cycles must be positive integers. Break duration must be non-negative.")
        sys.exit(1)

    run_timer(args.work, args.break, args.cycles)

if __name__ == "__main__":
    main()
