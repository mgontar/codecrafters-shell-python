import sys
import re

def main():

    # Never ending REPL loop
    while True:
        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()

        # Check for exit command
        pattern = r"^exit\s+(\d{1})"
        match = re.search(pattern, user_input)
        if match:
            exit_code = int(match.group(1))
            sys.exit(exit_code)

        # Format an output
        output = f"{user_input}: command not found"

        # Print an output
        print(output)


if __name__ == "__main__":
    main()
