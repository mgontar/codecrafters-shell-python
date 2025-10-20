import subprocess
import sys
import re
import os
from pathlib import Path

def get_executables(name):
    executables_list = []

    path_variable = os.getenv("PATH", "")
    path_list = path_variable.split(os.pathsep)

    for path in path_list:
        if os.path.isdir(path):
            files = [f for f in Path(path).iterdir() if f.is_file()]
            for file in files:
                if os.access(file, os.X_OK) and file.name == name:
                    executables_list.append(file)
    return executables_list

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

            if arg in builtin_commands_list:
                command_handled = True
                output = f"{arg} is a shell builtin"
                print(output)

            if not command_handled:
                executables_list = get_executables(arg)
                if len(executables_list) > 0:
                    command_handled = True
                    output = f"{arg} is {executables_list[0]}"
                    print(output)
                else:
                    output = f"{arg}: not found"
                    print(output)

        if not command_detected:
            pattern = r"^(\w+)\s*(.*)"
            match = re.search(pattern, user_input)
            if match:
                arg_name = match.group(1)
                arg_string = match.group(2)
                arg_list = arg_string.split()
                arg_list_out = [s.strip() for s in arg_list]
                executables_list = get_executables(arg_name)

                if len(executables_list) > 0:
                    arg_list_out.insert(0, executables_list[0].name)
                    subprocess.run(arg_list_out)
                else:
                    # Format an output
                    output = f"{user_input}: command not found"
                    # Print an output
                    print(output)
            else:
                # Format an output
                output = f"{user_input}: command not found"
                # Print an output
                print(output)


if __name__ == "__main__":
    main()
