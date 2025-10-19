import sys


def main():

    # Never ending REPL loop
    while True:
        # Print a prompt
        sys.stdout.write("$ ")

        # Read for user input
        user_input = input()

        # Format an output
        output = f"{user_input}: command not found"

        # Print an output
        print(output)


if __name__ == "__main__":
    main()
