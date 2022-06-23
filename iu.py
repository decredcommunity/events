from datetime import datetime
import os
from urllib.parse import urlparse

import strictyaml


class Config:
    indexdir    = "index"
    builddir    = "index"


class IuError(Exception):
    pass


class Const:
    index       = "index"


## I/O


def load_str(path):
    with open(path) as f:
        return f.read()


def load_yaml(path):
    return strictyaml.load(load_str(path))


def write_str(path, s):
    # Overwrite existing file.
    with open(path, "w", newline="\n") as f:
        f.write(s)


def init_build_dir(path):
    if not os.path.exists(path):
        os.mkdir(path, mode=0o700)
        print("Created directory:", path)


## Formats


def parse_date(s):
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise IuError("Unknown date format: " + s)


LANGUAGES = {
    "ar": "Arabic",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "zh": "Chinese",
}


## Site utils


SITES = {
    "facebook.com"  : "Facebook",
    "instagram.com" : "Instagram",
    "matrix.to"     : "Matrix",
    "pscp.tv"       : "Periscope",
    "twitter.com"   : "Twitter",
    "youtube.com"   : "YouTube",
}


def hostname(url):
    host = urlparse(url).hostname
    # Strip www.
    hostnw = host[len("www."):] if host.startswith("www.") else host
    return hostnw


def site_name(url):
    host = hostname(url)
    name = host
    if host in SITES:
        name = SITES[host]
    return name


def twitter_username(url):
    segments = urlparse(url).path.split("/")
    return segments[1]


## Generic Markdown utils


SEP = "\n"


def md_blank(l):
    l.append(SEP)


def md_parag(l, s, preblank=True):
    if preblank:
        md_blank(l)
    # Don't add an extra sep if `s` already has it.
    sep = "" if s.endswith("\n") else SEP
    l.append(s + sep)


def md_heading(l, level, s, preblank=True):
    md_parag(l, ("#" * level) + " " + s, preblank)


def md_begin_list(l):
    md_blank(l)


def md_li(l, s):
    l.append("- " + s + SEP)


def md_list(l, items):
    md_begin_list(l)
    for it in items:
        md_li(l, it)


def md_link(text, url):
    return "[{}]({})".format(text, url)


## Event-specific Markdown utils


def md_titlesx(l, data, lang_codes):
    for code in lang_codes:
        if not code == "en":
            titlex = data.get("title_" + code)
            if titlex:
                md_li(l, "title in {}: {}".format(LANGUAGES[code], titlex))


def md_announcements(l, anns):
    tweets, nontweets = [], []
    for aurl in anns:
        if hostname(aurl) == "twitter.com":
            tweets.append(md_link("@" + twitter_username(aurl), aurl))
        else:
            nontweets.append(aurl)
    items = []
    if tweets:
        items.append("tweets: " + ", ".join(tweets))
    for url in nontweets:
        items.append(md_link(site_name(url), url))
    md_list(l, items)


def md_media(l, media):
    items = []
    for m in media:
        if isinstance(m, str):
            murl = m
        elif isinstance(m, dict):
            murl = m["url"]
        items.append(md_link(site_name(murl), murl))
    md_list(l, items)


def md_optionals(l, data):
    desc = data.get("description")
    if desc:
        md_parag(l, desc)

    anns = data.get("announcements")
    if anns:
        md_parag(l, "Announcements:")
        md_announcements(l, anns)

    attendance = data.get("attendance")
    if attendance:
        md_parag(l, "Attendance:")
        md_list(l, attendance)

    media = data.get("media")
    if media:
        md_parag(l, "Media:")
        md_media(l, media)

    notes = data.get("notes")
    if notes:
        md_parag(l, "Notes:")
        md_list(l, notes)


def entry_md(eid, data):
    """Render one index entry as Markdown."""
    l = []
    md_parag(l, "back to [index]({}.md)".format(Const.index), preblank=False)
    # Required fields are accessed without testing to trigger an error if
    # missing.
    md_heading(l, 1, data["title"])

    # Begin key fields.
    md_begin_list(l)

    langs_str = data["lang"]
    lang_codes = langs_str.split(", ")
    if not lang_codes:
        raise IuError("At least 1 language is required in `lang`")
    lang_names = []
    for code in lang_codes:
        lang_name = LANGUAGES.get(code)
        if not lang_name:
            raise IuError("Unknown language code: " + code)
        lang_names.append(lang_name)
    md_li(l, "language: " + ", ".join(lang_names))

    md_titlesx(l, data, lang_codes)

    md_li(l, "start UTC: " + data["start_utc"])
    end_utc = data.get("end_utc")
    if end_utc:
        md_li(l, "end UTC: " + end_utc)

    md_li(l, "location: " + data["location"])

    orgs = []
    for org in data["organizers"]:
        ostr = "[{}]({})".format(org["org"], org["url"])
        if "person" in org:
            ostr += " ({})".format(org["person"])
        orgs.append(ostr)
    md_li(l, "organizers: " + ", ".join(orgs))

    md_li(l, "Decred participants: " + ", ".join(data["decred_people"]))

    # End key fields. Begin optional fields.

    md_optionals(l, data)

    subevents = data.get("subevents")
    if subevents:
        md_heading(l, 2, "Subevents")
        for subevent in subevents:
            md_heading(l, 3, subevent["title"])

            # Begin key fields.
            md_begin_list(l)

            md_titlesx(l, subevent, lang_codes)

            substart = subevent.get("start_utc")
            if substart:
                md_li(l, "start UTC: " + substart)

            subend = subevent.get("end_utc")
            if subend:
                md_li(l, "end UTC: " + subend)

            subpresenters = subevent.get("presenters")
            if subpresenters:
                md_li(l, "presenters: " + subpresenters)

            # End key fields. Begin optional fields.

            md_optionals(l, subevent)

    return "".join(l)


def index_md(entries):
    """Build top-level Markdown index page."""
    l = []
    md_heading(l, 1, "Decred Events", preblank=False)
    md_parag(l,
        "This is the index of past Decred events. Pages are generated from"
        " YAML files. To list your event please follow"
        " [these instructions]("
        "https://github.com/decredcommunity/events/blob/master/docs/submit-index.md).")

    year, month = None, None
    for eid, yaml in sorted(entries.items(), reverse=True):
        data = yaml.data
        date = parse_date(data["start_utc"])

        # Start new group when month changes.
        if not (year == date.year and month == date.month):
            year, month = date.year, date.month
            md_heading(l, 2, date.strftime("%B %Y"))
            md_begin_list(l)

        item = "{date}: [{title}]({eid}.md) ({people})".format(
            date=date.strftime("%b-%d"),
            title=data["title"],
            eid=eid,
            people=", ".join(data["decred_people"]))
        md_li(l, item)

    return "".join(l)


def write_md(outdir, basename, s):
    filename = basename + ".md"
    filepath = os.path.join(outdir, filename)
    write_str(filepath, s)
    print("Wrote", filename)


## Command-line interface


def build_md(args):
    outdir = args.outdir
    init_build_dir(outdir)
    indexdir = args.path

    entries = {}

    for curdir, dirs, files in os.walk(indexdir):
        for filename in files:
            if filename.endswith(".yml") and (not filename == "0_template.yml"):
                filepath = os.path.join(curdir, filename)
                eid = filename.replace(".yml", "")
                yaml = load_yaml(filepath)
                entries[eid] = yaml

    print("Loaded {} entries".format(len(entries)))
    print("Writing to directory:", outdir)

    wrote_count = 0
    for eid, yaml in entries.items():
        try:
            emd = entry_md(eid, yaml.data)
            write_md(outdir, eid, emd)
            wrote_count += 1
        except IuError as e:
            print("Error in {}: {}".format(eid, str(e)))

    write_md(outdir, Const.index, index_md(entries))
    wrote_count += 1
    print("Wrote {} files".format(wrote_count))


def make_arg_parser():
    import argparse

    parser = argparse.ArgumentParser(description="Index utility")
    parser.set_defaults(cmd=lambda _args: parser.print_usage())

    subparsers = parser.add_subparsers(dest="command", title="commands")

    md = subparsers.add_parser(
        "md",
        help="Generate Markdown from index files")
    md.add_argument(
        "path", nargs="?",
        default=Config.indexdir,
        help="Directory with input .yml files (default: {})"
             "".format(Config.indexdir))
    md.add_argument(
        "-o", "--outdir",
        default=Config.builddir,
        help="Output directory for generated .md files (default: {})"
             "".format(Config.builddir))
    md.set_defaults(cmd=build_md)

    return parser


def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    try:
        args.cmd(args)
    except KeyboardInterrupt:
        # Handle Ctrl-C.
        print("\nAborting")
    except BrokenPipeError:
        # Silence error when e.g. piping into `less` and quitting before
        # reading all.
        pass
    except IuError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
