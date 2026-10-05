import argparse
import json
from pathlib import Path
import shlex


DB_FILE = "lilkv.jsonl"


def init_file():
    file_path = Path(DB_FILE)
    if not file_path.exists():
        file_path.touch()


def write(key, value):
    with open(DB_FILE, "a") as f:
        f.write(json.dumps({key: value}) + "\n")


def read(key):
    with open(DB_FILE, "r") as f:
        lines = f.readlines()
        value = None
        for line in lines:
            json_line = json.loads(line)
            value = json_line.get(key, value)
        return value


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lilkv",
        description="Little file based key-value database.",
        exit_on_error=False
    )
    parser.add_argument("command", choices=["get", "set"])
    parser.add_argument("key", type=str)
    parser.add_argument("value", type=str, nargs="?", default=None)
    return parser


def parse_args(parser, cli_args):
    args = None
    try:
        args = parser.parse_args(shlex.split(cli_args))
    except argparse.ArgumentError as exc:
        print(exc)
    except ValueError as exc:
        print(exc)
    except SystemExit:
        pass
    return args


def run():
    init_file()
    parser = build_parser()

    while True:
        try:
            cli_args = input("lilkv>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if not cli_args:
            continue

        args = parse_args(parser, cli_args)
        if not args:
            continue

        if args.command == "get":
            print(read(args.key))
        if args.command == "set":
            write(args.key, args.value)


if __name__ == "__main__":
    run()
