import os
import sys

def check_env_vars(required_vars_str: str) -> bool:
    """
    Checks for the presence and non-emptiness of specified environment variables.

    Args:
        required_vars_str: A comma-separated string of environment variable names.

    Returns:
        True if all required variables are present and non-empty, False otherwise.
    """
    required_vars = [v.strip() for v in required_vars_str.split(',') if v.strip()]
    
    if not required_vars:
        print("No required environment variables specified.")
        return True

    all_present_and_non_empty = True
    print(f"--- Nightly Env-Var Enforcement Report ---")

    for var_name in required_vars:
        value = os.environ.get(var_name)
        if value is None:
            print(f"❌ MISSING: Environment variable '{var_name}' is not set.")
            all_present_and_non_empty = False
        elif not value:
            print(f"⚠️ EMPTY: Environment variable '{var_name}' is set but empty.")
            all_present_and_non_empty = False
        else:
            print(f"✅ PRESENT: Environment variable '{var_name}' is set and non-empty.")
    
    print(f"------------------------------------------")
    if all_present_and_non_empty:
        print("All required environment variables are present and non-empty. Good to go!")
    else:
        print("Some required environment variables are missing or empty. Please address them.")

    return all_present_and_non_empty

def main():
    if len(sys.argv) < 2:
        print("Usage: python enforcer.py <comma_separated_required_env_vars>")
        sys.exit(1)
    
    required_vars_str = sys.argv[1]
    if not check_env_vars(required_vars_str):
        sys.exit(1) # Exit with non-zero for failure

if __name__ == "__main__":
    main()
