class Config:
    index_dir   = "index"
    build_dir   = "build"

def build_md(args):
    raise Exception("Not implemented yet!")

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
        "-o", "--output",
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
