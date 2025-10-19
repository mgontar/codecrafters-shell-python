import sys


def main():
    # Print prompt
    sys.stdout.write("$ ")

    # Read for user input
    user_input = input()

    # Print output
    print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()
