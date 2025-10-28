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


def unescape_double(s):
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt in ['"', '\\', '$', '`']:
                out.append(nxt)
                i += 2
                continue
            elif nxt == '\n':  # line continuation
                i += 2
                continue
        out.append(ch)
        i += 1
    return ''.join(out)


def unescape_unquoted(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            out.append(s[i + 1])
            i += 2
        else:
            out.append(s[i])
            i += 1
    return ''.join(out)


def command_echo(arg_string):
    # Keep your normalizations
    arg_string = arg_string.replace("''", "")
    arg_string = arg_string.replace('""', "")
    arg_string = re.sub(r"'\s+'", " ", arg_string)
    arg_string = re.sub(r'"\s+"', " ", arg_string)

    # Capture any leading whitespace *per token* as group(1)
    pattern = re.compile(r"""
        (\s*)(
            '([^']*)'                    |   # single-quoted literal
            "((?:[^"\\]|\\.)*)"          |   # double-quoted with limited escapes
            ((?:\\.|[^\s"'\\])+)
        )
    """, re.X)

    pieces = []
    for m in pattern.finditer(arg_string):
        had_ws = bool(m.group(1))
        single = m.group(3)
        dbl = m.group(4)
        unq = m.group(5)

        if single is not None:
            val = single
        elif dbl is not None:
            val = unescape_double(dbl)
        else:
            val = unescape_unquoted(unq)

        if had_ws and pieces:
            pieces.append(' ')  # only add a space if there *was* whitespace
        pieces.append(val)

    output = ''.join(pieces)
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


def execute(command, args, stdout_file):
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
        if stdout_file is None:
            subprocess.run(arg_list_out)
        else:
            subprocess.run(arg_list_out, stdout=stdout_file)
    else:
        output = f"{command} {args}: command not found"
        print(output)


def main():
    # print(os.environ["PATH"])
    # Never ending REPL loop
    while True:
        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()
        command = ""
        args = ""
        pattern = r"(?:(?:'(.+)')|(?:\"(.+)\")|(\S+))(?:\s+(.+))?"
        match = re.search(pattern, user_input)
        if match:
            cmd_sq = match.group(1)
            cmd_dq = match.group(2)
            cmd_nq = match.group(3)
            command = cmd_nq if cmd_nq is not None else cmd_sq if cmd_sq is not None else cmd_dq
            args = match.group(4)
            args = args if args is not None else ""
        else:
            idx = user_input.find(" ")
            if idx == -1:
                command = user_input.strip()
                args = ""
            else:
                command = user_input[:idx].strip()
                args = user_input[idx + 1:].strip()

        # Process output redirection
        old_stdout = sys.stdout
        out_file = None
        pattern = r"(.+)(?:(?:\s+1>\s+)|(?:\s+>\s+))(.+)"
        match = re.search(pattern, args)
        if match:
            args = match.group(1)
            redirect_path = match.group(2)
            #print(f'{args}')
            #print(f'{redirect_path}')
            out_file = open(redirect_path, 'w')
            sys.stdout = out_file

        if command:
            if command in builtin_commands_dict:
                builtin_commands_dict[command](args)
            elif len(get_executables(command)) > 0:
                execute(command, args, out_file)
            else:
                output = f"{user_input}: command not found"
                print(output)

        # Restore output
        sys.stdout = old_stdout


if __name__ == "__main__":
    main()
