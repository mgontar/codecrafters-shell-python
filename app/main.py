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

        # Check for exit command
        pattern = r"^echo\s+(.+)"
        match = re.search(pattern, user_input)
        if match:
            args_string = match.group(1)
            args_list = args_string.split()
            args_list_out = [s.strip() for s in args_list]
            args_string_out = " ".join(args_list_out)
            output = f"{args_string_out}"
            print(output)
        else:
            # Format an output
            output = f"{user_input}: command not found"
            # Print an output
            print(output)


if __name__ == "__main__":
    main()
