import argparse
import json
import subprocess
import sys
import time

def record_command_output(image: str, command: str, output_file: str):
    """
    Runs a command in a Docker container and records its stdout, stderr, and exit code.
    """
    print(f"Recording command '{command}' in image '{image}'...")
    try:
        # Construct the docker run command
        docker_cmd = [
            "docker", "run", "--rm",  # --rm removes the container after exit
            image,
            "bash", "-c", command # Execute command via bash -c to handle complex commands
        ]
        
        # Execute the command
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            check=False # Do not raise an exception for non-zero exit codes
        )

        output_data = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "image": image,
            "command": command,
            "timestamp": time.time()
        }

        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"Successfully recorded output to {output_file}")
        print(f"Exit Code: {result.returncode}")

    except FileNotFoundError:
        print("Error: 'docker' command not found. Is Docker installed and in your PATH?", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running Docker command: {e}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during recording: {e}", file=sys.stderr)
        sys.exit(1)

def replay_command_output(input_file: str, delay: float = 0.01):
    """
    Replays previously recorded command output from a JSON file.
    """
    print(f"Replaying output from {input_file}...")
    try:
        with open(input_file, 'r') as f:
            output_data = json.load(f)
        
        stdout = output_data.get("stdout", "")
        stderr = output_data.get("stderr", "")
        exit_code = output_data.get("exit_code", 0)
        original_image = output_data.get("image", "N/A")
        original_command = output_data.get("command", "N/A")
        
        print(f"\n--- Replay of '{original_command}' from '{original_image}' ---")
        
        if stdout:
            print("\n--- STDOUT ---")
            for char in stdout:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(delay)
            print() # Ensure newline at the end
        
        if stderr:
            print("\n--- STDERR ---")
            for char in stderr:
                sys.stderr.write(char)
                sys.stderr.flush()
                time.sleep(delay)
            print() # Ensure newline at the end
            
        print(f"--- Replay Finished (Simulated Exit Code: {exit_code}) ---\n")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{input_file}'. Is it a valid recording?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during replaying: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Docker Echo Replay: Capture and replay command output from Docker containers."
    )
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode", required=True)

    # Record mode parser
    record_parser = subparsers.add_parser("record", help="Record command output from a Docker container.")
    record_parser.add_argument("--image", required=True, help="Docker image to run the command in (e.g., 'ubuntu:latest').")
    record_parser.add_argument("--command", required=True, help="Command to execute inside the Docker container.")
    record_parser.add_argument("--output", required=True, help="Path to save the recorded output JSON file.")

    # Replay mode parser
    replay_parser = subparsers.add_parser("replay", help="Replay previously recorded command output.")
    replay_parser.add_argument("--input", required=True, help="Path to the recorded output JSON file.")
    replay_parser.add_argument("--delay", type=float, default=0.01, help="Simulated typing delay between characters (seconds).")

    args = parser.parse_args()

    if args.mode == "record":
        record_command_output(args.image, args.command, args.output)
    elif args.mode == "replay":
        replay_command_output(args.input, args.delay)

if __name__ == "__main__":
    main()
