import os

from datetime import datetime

import strictyaml

class IuError(Exception):
    pass

class Config:
    index_dir   = "index"
    build_dir   = "build"

class Const:
    index       = "index"

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

def entry_md(eid, data):
    """Render one index entry as Markdown"""
    md = "back to [index]({}.md)\n\n".format(Const.index)
    md += "# {}\n\n".format(data["title"])
    md += "- language: {}\n".format(data["lang"])
    md += "- start UTC: {}\n".format(data["start_utc"])
    if "end_utc" in data:
        md += "- end UTC: {}\n".format(data["end_utc"])
    md += "- location: {}\n".format(data["location"])
    orgs = []
    for org in data["organizers"]:
        ostr = "[{}]({})".format(org["org"], org["url"])
        if "person" in org:
            ostr += " ({})".format(org["person"])
        orgs.append(ostr)
    md += "- organizers: {}\n".format(", ".join(orgs))
    md += "- Decred participants: {}\n\n".format(", ".join(data["decred_people"]))
    md += data["description"] + "\n\n"
    if "announcements" in data:
        md += "Announcements:\n\n"
        for ann in data["announcements"]:
            md += "- {}\n".format(ann)
        md += "\n"
    if "attendance" in data:
        md += "Attendance:\n\n"
        for a in data["attendance"]:
            md += "- {}\n".format(a)
        md += "\n"
    if "media" in data:
        md += "Media:\n\n"
        for m in data["media"]:
            if isinstance(m, str):
                md += "- {}\n".format(m)
            elif isinstance(m, dict):
                md += "- {}\n".format(m["url"])
        md += "\n"
    if "notes" in data:
        md += "Notes:\n\n"
        for n in data["notes"]:
            md += "- {}\n".format(n)
        md += "\n"
    return md

def index_md(entries):
    """Build top-level Markdown index page"""
    md = "# Index of events\n\n"
    for eid, yaml in sorted(entries.items(), reverse=True):
        data = yaml.data
        date = parse_date(data["start_utc"])
        date_str = date.strftime("%Y-%b-%d")
        item = "- {date}: [{title}]({eid}.md)\n".format(
            date=date_str, title=data["title"], eid=eid)
        md += item
    return md

def write_md(out_dir, basename, s):
    filename = basename + ".md"
    filepath = os.path.join(out_dir, filename)
    write_str(filepath, s)
    print("wrote", filename)

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

    for eid, yaml in entries.items():
        write_md(out_dir, eid, entry_md(eid, yaml.data))

    write_md(out_dir, Const.index, index_md(entries))

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
