import os

import strictyaml

class Config:
    index_dir   = "index"
    build_dir   = "build"

def load_str(path):
    with open(path) as f:
        return f.read()

def load_yaml(path):
    return strictyaml.load(load_str(path))

def init_build_dir(path):
    if not os.path.exists(path):
        os.mkdir(path, mode=0o700)
        print("created directory '{}'".format(path))

def build_md(args):
    init_build_dir(args.outdir)
    indexdir = args.path
    for curdir, dirs, files in os.walk(indexdir):
        for filename in files:
            if filename.endswith(".yml") and (not filename == "0_template.yml"):
                filepath = os.path.join(curdir, filename)
                oid = filename.replace(".yml", "")
                yaml = load_yaml(filepath)
                print(oid, ":", yaml.data["title"])

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
