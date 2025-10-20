import sys
import re
import os
from pathlib import Path

def main():
    builtin_commands_list = ["exit", "echo", "type"]

    # Never ending REPL loop
    while True:

        command_detected = False

        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()

        # Check for exit command
        pattern = r"^exit\s+(\d{1})"
        match = re.search(pattern, user_input)
        if match:
            command_detected = True
            exit_code = int(match.group(1))
            sys.exit(exit_code)

        # Check for exit command
        pattern = r"^echo\s+(.+)"
        match = re.search(pattern, user_input)
        if match:
            command_detected = True
            args_string = match.group(1)
            args_list = args_string.split()
            args_list_out = [s.strip() for s in args_list]
            args_string_out = " ".join(args_list_out)
            output = f"{args_string_out}"
            print(output)

        # Check for exit command
        pattern = r"^type\s+(\w+)"
        match = re.search(pattern, user_input)
        if match:
            command_detected = True

            command_handled = False

            arg = match.group(1)

            path_variable = os.getenv("PATH", "")
            path_list = path_variable.split(os.pathsep)

            for path in path_list:
                if os.path.isdir(path):
                    files = [f for f in Path(path).iterdir() if f.is_file()]
                    for file in files:
                        if os.access(file, os.X_OK) and file.name == arg:
                            command_handled = True
                            output = f"{arg} is {file}"
                            print(output)
                            break
                    if command_handled:
                        break

            if not command_handled:
                if arg in builtin_commands_list:
                    output = f"{arg} is a shell builtin"
                    print(output)
                else:
                    output = f"{arg}: not found"
                    print(output)

        if not command_detected:
            # Format an output
            output = f"{user_input}: command not found"
            # Print an output
            print(output)


if __name__ == "__main__":
    main()
