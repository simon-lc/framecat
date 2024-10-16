import sys
from framecat.cli_interface import (
    parse_args,
    execute_command,
)


def main():
    args = parse_args(sys.argv[1:])
    execute_command(args)


if __name__ == "__main__":
    main()
