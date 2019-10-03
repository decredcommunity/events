## Before you start

Things to remember:

* This repository is **public**. Anyone can read both final reports and their drafts in the pull requests. Do not leak sensitive information.
* Your email can be extracted from Git commits. Read [this info](https://help.github.com/en/articles/setting-your-commit-email-address) to understand and configure which email address is recorded when you save documents on GitHub.
* Please don't commit images, they quickly grow the size of the repository (see below).

## 3 ways to submit

There are multiple ways to submit an event report depending on how familiar you are with GitHub and Git:

1. Submit a pull request (preferred)
2. Ask admins to create a draft that you can edit
3. Create a gist with the report and send it to admins

To submit changes to existing documents use options 1 or 2.

Reports are written in a format called Markdown. It is pretty simple, but for less common techniques there is an excellent [cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) that should be in your bookmarks.

## No images in Git

Please do not commit images (e.g. photos) or other large files into Git because it grows repository size too quickly. Instead, link to images hosted on in your signed Keybase public folder ([example](https://keybase.pub/jz_bz/)), Twitter, IPFS, etc.

File hosting is an open issue. Ultimately we need a robust and replicated [file archive](https://github.com/decredcommunity/issues/issues/26) but this is not available yet.

## 1. Submit a pull request

This way is most advanced but is also most flexible and requires less admin assistance.

1. [Fork](https://help.github.com/en/categories/collaborating-with-issues-and-pull-requests) the events repository.
2. Create a file with your report in the `reports` directory. The file name must follow the format `YYYYMMDD-title-city-country.md`, e.g. `20190116-tnabc-miami-usa.md`. You can use [this template](https://raw.githubusercontent.com/decredcommunity/events/docs/report-template.md) as a starting point.
3. Create a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) against the events repository.
  * Check `Allow edits from maintainers` ([help](https://help.github.com/en/articles/allowing-changes-to-a-pull-request-branch-created-from-a-fork)).
  * Optionally, use [Draft pull request](https://help.github.com/en/articles/about-pull-requests#draft-pull-requests) that cannot be merged until you mark it as ready.

## 2. Request a draft

This method is easier than previous, at the cost of some admin work. Unlike gists, it still allows others to be aware of your work on the report, and also allows multiple people to edit it.

1. [Contact admins](#contact-admins) and ask to create a draft for you.
2. You will be invited as a collaborator and provided with a link to the draft.
3. Edit the draft as necessary.
4. When finished, [create a pull request](https://help.github.com/en/articles/creating-a-pull-request) or ask to do it for you.

## 3. The gist way

Gist is most often a single versioned document and it is perfect for event reports. All you need is a GitHub account.

1. Visit https://gist.github.com/
2. Enter filename in this format: `YYYYMMDD-title-city-country.md`. Example: `20190116-tnabc-miami-usa.md`.
3. Enter report contents. You can use [this template](https://raw.githubusercontent.com/decredcommunity/events/docs/report-template.md).
4. Press `Create secret gist` or `Create public gist` depending on your preference. Secret gists can only be accessed knowing the correct link and are not listed in your profile.
5. Edit the gist as necessary.
6. When finished, [contact admins](#contact-admins) and ask to add your report to the repository.

Other ways to share a document would work too, but gist is

* better than chat message because it can be long and you can edit it
* better than [pastebin](https://en.wikipedia.org/wiki/Pastebin) services because it has clear version history
* better than Google Docs because it can be accessed without Google account and without executing a ton of proprietary code

Learn more about gists [here](https://help.github.com/en/articles/about-gists).

## Tell people about your report

When your report is processed and "merged" (kind of released), let people know about it. Use the final link in the master branch and:

1. Share it to other events people in #event\_planning chat room
2. Submit it to [r/decred](https://www.reddit.com/r/decred/) subreddit
3. Post it on your Twitter
4. Optionally, ask in #social\_media room to retweet

## Contact admins

To get your reports merged or to propose an improvement:

* submit a pull request as detailed above
* or [create an issue](https://github.com/decredcommunity/events/issues)
* or ask in #event\_planning chat room (ping @bee)

To propose a tweet or retweet of your report:

* ask in #social\_media chat room.

Chat rooms are available in [Matrix](https://decred.org/matrix/), [Discord](https://discord.gg/GJ2GXfz) or [Slack](https://slack.decred.org/).
