import subprocess
import sys
import os
from pathlib import Path

builtin_commands_dict = {}


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


def command_exit(arg_string):
    code = int(arg_string)
    sys.exit(code)


def command_echo(arg_string):
    arg_list = arg_string.split()
    arg_list_out = [s.strip() for s in arg_list]
    arg_string_out = " ".join(arg_list_out)
    output = f"{arg_string_out}"
    print(output)


def command_type(arg_string):
    if arg_string in builtin_commands_dict:
        output = f"{arg_string} is a shell builtin"
        print(output)
    else:
        executables_list = get_executables(arg_string)
        if len(executables_list) > 0:
            output = f"{arg_string} is {executables_list[0]}"
            print(output)
        else:
            output = f"{arg_string}: not found"
            print(output)


def command_pwd(user_input):
    current_directory = os.getcwd()
    print(current_directory)


def command_cd(arg):
    new_directory = arg
    if arg == "~":
        new_directory = os.path.expanduser("~")
    if os.path.isdir(new_directory):
        os.chdir(new_directory)
    else:
        output = f"cd: {new_directory}: No such file or directory"
        print(output)


builtin_commands_dict = {"exit": command_exit,
                         "echo": command_echo,
                         "type": command_type,
                         "pwd": command_pwd,
                         "cd": command_cd}


def execute(user_input):
    arg_list = user_input.split()
    arg_list_out = [s.strip() for s in arg_list]
    executables_list = get_executables(arg_list_out[0])
    if len(executables_list) > 0:
        subprocess.run(arg_list_out)
    else:
        output = f"{user_input}: command not found"
        print(output)


def main():
    # Never ending REPL loop
    while True:
        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()
        args_list = user_input.split()
        if len(args_list) > 0:
            if args_list[0] in builtin_commands_dict:
                builtin_commands_dict[args_list[0]](" ".join(args_list[1:]))
            elif len(get_executables(args_list[0])) > 0:
                execute(user_input)
            else:
                output = f"{user_input}: command not found"
                print(output)


if __name__ == "__main__":
    main()
