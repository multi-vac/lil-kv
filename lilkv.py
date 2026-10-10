import argparse
import json
from pathlib import Path
import shlex


DB_FILE = "lilkv.jsonl"
INDEX = {}


def init_file():
    file_path = Path(DB_FILE)
    if not file_path.exists():
        file_path.touch()


def write(key, value):
    with open(DB_FILE, "ab") as f:
        current_position = f.tell()
        f.write((json.dumps({key: value}) + "\n").encode())
        add_to_index(key, current_position)


def read(key):
    try:
        return read_from_index(key)
    except KeyError:
        pass

    with open(DB_FILE, "rb") as f:
        lines = f.readlines()
        value = None
        for line in lines:
            json_line = json.loads(line)
            value = json_line.get(key, value)
        return value


def build_index():
    with open(DB_FILE, "rb") as f:
        current_position = 0
        for line in f:
            key = next(iter(json.loads(line).keys()))
            add_to_index(key, current_position)
            current_position = f.tell()


def add_to_index(key, current_position):
    INDEX[key] = current_position
    print(f"Added {key} to {current_position}")


def read_from_index(key):
    if key not in INDEX:
        raise KeyError

    with open(DB_FILE, "rb") as f:
        f.seek(INDEX[key])
        value = json.loads(f.readline())[key]
        print(f"Read {key} from {INDEX[key]} with value {value}")
        return value


def build_parser():
    parser = argparse.ArgumentParser(
        prog="lilkv",
        description="A little append-only key-value database",
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
    build_index()
    parser = build_parser()

    while True:
        try:
            cli_args = input("lil-kv>> ").strip()
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
