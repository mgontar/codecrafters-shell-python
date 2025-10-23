import subprocess
import sys
import os
import re
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


def unescape(s):
    """Unescape sequences inside double quotes."""
    return bytes(s, "utf-8").decode("unicode_escape")


def command_echo(arg_string):
    arg_string = arg_string.replace("''", "")
    arg_string = arg_string.replace('""', "")
    arg_string = re.sub(r"'\s+'", " ", arg_string)
    arg_string = re.sub(r'"\s+"', " ", arg_string)

    pattern = re.compile(r"""
        \s*(
            '([^']*)'                        |   # single-quoted literal
            "((?:[^"\\]|\\.)*)"              |   # double-quoted with escapes
            ((?:\\.|[^\s"'\\])+ )                # unquoted token
        )
    """, re.X)

    tokens = []
    for m in pattern.finditer(arg_string):
        single, double, unquoted = m.group(2), m.group(3), m.group(4)
        if single is not None:
            val = single  # treat literally
        elif double is not None:
            val = unescape(double)
        else:
            val = unescape(unquoted)
        tokens.append(val)
    output = " ".join(tokens)
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


def unescape(s: str) -> str:
    # remove backslash escapes: \x -> x
    return re.sub(r'\\(.)', r'\1', s)


def execute(command, args):
    arg_list_out = []
    pattern = re.compile(r"'([^']*)'|\"([^\"]*)\"|(\S+)")
    tokens = []
    for m in pattern.finditer(args):
        val = next(g for g in m.groups() if g is not None)
        tokens.append(val)
    if len(tokens) > 0:
        arg_list_out = tokens
    else:
        arg_list = args.split()
        arg_list_out = [s.strip() for s in arg_list]
    executables_list = get_executables(command)
    if len(executables_list) > 0:
        arg_list_out.insert(0, command)
        subprocess.run(arg_list_out)
    else:
        output = f"{command} {args}: command not found"
        print(output)


def main():
    # Never ending REPL loop
    while True:
        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()

        idx = user_input.find(" ")
        if idx == -1:
            command = user_input.strip()
            args = ""
        else:
            command = user_input[:idx].strip()
            args = user_input[idx + 1:].strip()

        if command:
            if command in builtin_commands_dict:
                builtin_commands_dict[command](args)
            elif len(get_executables(command)) > 0:
                execute(command, args)
            else:
                output = f"{user_input}: command not found"
                print(output)


if __name__ == "__main__":
    main()
