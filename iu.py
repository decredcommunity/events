import os

from datetime import datetime

import strictyaml

class IuError(Exception):
    pass

class Config:
    index_dir   = "index"
    build_dir   = "build"

def load_str(path):
    with open(path) as f:
        return f.read()

def load_yaml(path):
    return strictyaml.load(load_str(path))

def write_str(path, s):
    # overwrite existing file
    with open(path, "w", newline="\n") as f:
        f.write(s)

def init_build_dir(path):
    if not os.path.exists(path):
        os.mkdir(path, mode=0o700)
        print("created directory '{}'".format(path))

def parse_date(s):
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise IuError("unknown date format: " + s)

def index_md(entries):
    """Build top-level Markdown index page"""
    md = "# Index of events\n\n"
    for eid, yaml in sorted(entries.items(), reverse=True):
        data = yaml.data
        date = parse_date(data["start_utc"])
        date_str = date.strftime("%Y-%b-%d")
        item = "- {date}: {title}\n".format(
            date=date_str, title=data["title"])
        md += item
    return md

def build_md(args):
    out_dir = args.outdir
    init_build_dir(out_dir)
    indexdir = args.path

    entries = {}

    for curdir, dirs, files in os.walk(indexdir):
        for filename in files:
            if filename.endswith(".yml") and (not filename == "0_template.yml"):
                filepath = os.path.join(curdir, filename)
                eid = filename.replace(".yml", "")
                yaml = load_yaml(filepath)
                entries[eid] = yaml

    print("writing to:", out_dir)
    index_str = index_md(entries)
    index_filename = "index.md"
    index_filepath = os.path.join(out_dir, index_filename)
    write_str(index_filepath, index_str)
    print("wrote", index_filename)

def make_arg_parser():
    import argparse

    parser = argparse.ArgumentParser(description="index utility")
    subparsers = parser.add_subparsers(dest="command", title="commands")

    md = subparsers.add_parser(
        "md",
        help="generate Markdown from index files")
    md.add_argument(
        "path", nargs="?",
        default=Config.index_dir,
        help="index directory with input YAML files, '{}' by default"
            .format(Config.index_dir))
    md.add_argument(
        "-o", "--outdir",
        default=Config.build_dir,
        help="output dir for generated Markdown files, '{}' by default"
            .format(Config.build_dir))
    md.set_defaults(func=build_md)

    return parser

def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    if args.command:
        try:
            args.func(args)
        except Exception as e:
            # todo: replace with your custom exception type
            print("error:", e)
        except KeyboardInterrupt:
            # handle Ctrl-C
            print("\naborting")
        except BrokenPipeError:
            # silence error when e.g. piping into `less` and quitting before
            # reading all
            pass
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
