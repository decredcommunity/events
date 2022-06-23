import os

from datetime import datetime
from urllib.parse import urlparse

import strictyaml

class IuError(Exception):
    pass

class Config:
    indexdir   = "index"
    builddir   = "index"

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
        print("created directory:", path)

def parse_date(s):
    for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    raise IuError("unknown date format: " + s)

LANGUAGES = {
    "ar": "Arabic",
    "en": "English",
    "es": "Spanish",
    "pt": "Portuguese",
    "zh": "Chinese",
}

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
    # strip www.
    hostnw = host[len("www."):] if host.startswith("www.") else host
    return hostnw

def site_name(url):
    host = hostname(url)
    if host in SITES:
        return SITES[host]
    return host

def twitter_username(url):
    segments = urlparse(url).path.split("/")
    return segments[1]

def list_md(items, indent=0):
    md = ""
    indentstr = "  " * indent
    for it in items:
        md += indentstr + "- {}\n".format(it)
    return md

def paragraph_md(p):
    md = p
    if not p.endswith("\n"):
        md += "\n"      # if it doesn't have its own line ending, add it
    return md

def announcements_md(anns, indent=0):
    md = ""
    indentstr = "  " * indent
    tweets, nontweets = [], []
    for aurl in anns:
        if hostname(aurl) == "twitter.com":
            tweets.append("[@{}]({})".format(twitter_username(aurl), aurl))
        else:
            nontweets.append(aurl)
    if tweets:
        md += indentstr + "- tweets: {}\n".format(", ".join(tweets))
    for url in nontweets:
        md += indentstr + "- [{}]({})\n".format(site_name(url), url)
    return md

def media_md(medias, indent=0):
    md = ""
    indentstr = "  " * indent
    for m in medias:
        if isinstance(m, str):
            murl = m
        elif isinstance(m, dict):
            murl = m["url"]
        md += indentstr + "- [{}]({})\n".format(site_name(murl), murl)
    return md

def titlesx_md(data, lang_codes):
    md = ""
    for code in lang_codes:
        if not code == "en":
            titlex = data.get("title_" + code)
            if titlex:
                md += "- title in {}: {}\n".format(LANGUAGES[code], titlex)
    return md

def entry_md(eid, data):
    """Render one index entry as Markdown"""
    md = "back to [index]({}.md)\n\n".format(Const.index)
    # required fields are accessed without testing to trigger an error if
    # missing
    md += "# {}\n\n".format(data["title"])
    # begin key stats
    langs_str = data["lang"]
    lang_codes = langs_str.split(", ")
    if not lang_codes:
        raise IuError("at least one language is required in `lang`")
    lang_names = []
    for code in lang_codes:
        lang_name = LANGUAGES.get(code)
        if not lang_name:
            raise IuError("unknown language code: " + code)
        lang_names.append(lang_name)

    md += "- language: {}\n".format(", ".join(lang_names))
    titlesx = titlesx_md(data, lang_codes)
    if titlesx:
        md += titlesx

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
    md += "- Decred participants: {}\n".format(", ".join(data["decred_people"]))
    # end key stats
    if "description" in data:
        md += "\n"
        desc = data["description"]
        md += paragraph_md(desc)
    if "announcements" in data:
        md += "\n"
        md += "Announcements:\n\n"
        md += announcements_md(data["announcements"])
    if "attendance" in data:
        md += "\n"
        md += "Attendance:\n\n"
        md += list_md(data["attendance"])
    if "media" in data:
        md += "\n"
        md += "Media:\n\n"
        md += media_md(data["media"])
    if "notes" in data:
        md += "\n"
        md += "Notes:\n\n"
        md += list_md(data["notes"])
    if "subevents" in data:
        md += "\n"
        md += "## Subevents\n"
        for subevent in data["subevents"]:
            subtitle = subevent["title"]
            md += "\n"
            md += "### {}\n\n".format(subtitle)
            # begin key stats
            subtitlesx = titlesx_md(subevent, lang_codes)
            if subtitlesx:
                md += subtitlesx
            substart = subevent.get("start_utc")
            if substart:
                md += "- start UTC: {}\n".format(substart)
            subend = subevent.get("end_utc")
            if subend:
                md += "- end UTC: {}\n".format(subend)
            subpresenters = subevent.get("presenters")
            if subpresenters:
                md += "- presenters: {}\n".format(subpresenters)
            # end key stats
            subdesc = subevent.get("description")
            if subdesc:
                md += "\n"
                md += paragraph_md(subdesc)
            subanns = subevent.get("announcements")
            if subanns:
                md += "\n"
                md += "Announcements:\n\n"
                md += announcements_md(subanns)
            subatt = subevent.get("attendance")
            if subatt:
                md += "\n"
                md += "Attendance:\n\n"
                md += list_md(subatt)
            submedia = subevent.get("media")
            if submedia:
                md += "\n"
                md += "Media:\n\n"
                md += media_md(submedia)
            subnotes = subevent.get("notes")
            if subnotes:
                md += "\n"
                md += "Notes:\n\n"
                md += list_md(subnotes)
    return md

def index_md(entries):
    """Build top-level Markdown index page"""
    md = ("# Decred Events\n\n"
          "This is the index of past Decred events. "
          "Pages are generated from YAML files. "
          "To list your event please follow [these instructions](https://github.com/decredcommunity/events/blob/master/docs/submit-index.md).\n")
    year, month = None, None
    for eid, yaml in sorted(entries.items(), reverse=True):
        data = yaml.data
        date = parse_date(data["start_utc"])
        # group by month
        if not (year == date.year and month == date.month):
            year, month = date.year, date.month
            md += "\n## {}\n\n".format(date.strftime("%B %Y"))
        item = "- {date}: [{title}]({eid}.md) ({people})\n".format(
            date=date.strftime("%b-%d"),
            title=data["title"],
            eid=eid,
            people=", ".join(data["decred_people"]))
        md += item
    return md

def write_md(outdir, basename, s):
    filename = basename + ".md"
    filepath = os.path.join(outdir, filename)
    write_str(filepath, s)
    print("wrote", filename)

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

    print("writing to directory:", outdir)

    for eid, yaml in entries.items():
        try:
            emd = entry_md(eid, yaml.data)
            write_md(outdir, eid, emd)
        except IuError as e:
            print("error in {}: {}".format(eid, str(e)))

    write_md(outdir, Const.index, index_md(entries))

def make_arg_parser():
    import argparse

    parser = argparse.ArgumentParser(description="index utility")
    subparsers = parser.add_subparsers(dest="command", title="commands")

    md = subparsers.add_parser(
        "md",
        help="generate Markdown from index files")
    md.add_argument(
        "path", nargs="?",
        default=Config.indexdir,
        help="index directory with input YAML files, '{}' by default"
            .format(Config.indexdir))
    md.add_argument(
        "-o", "--outdir",
        default=Config.builddir,
        help="output dir for generated Markdown files, '{}' by default"
            .format(Config.builddir))
    md.set_defaults(func=build_md)

    return parser

def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    if args.command:
        try:
            args.func(args)
        except KeyboardInterrupt:
            # handle Ctrl-C
            print("\naborting")
        except BrokenPipeError:
            # silence error when e.g. piping into `less` and quitting before
            # reading all
            pass
        except IuError as e:
            print("error:", e)
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
