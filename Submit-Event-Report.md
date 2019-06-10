There are multiple ways to submit an event report depending on how familiar you are with GitHub and Git:

1. Create a gist with the report and send it to admins of this repo
2. Ask admins to give you a draft you can edit
3. Submit a pull request

To submit changes to existing reports, options 2 and 3 apply.

Note: read [this info](https://help.github.com/en/articles/about-commit-email-addresses) to understand and configure which email address is recorded when you save documents on GitHub.

Reports are written in a format called Markdown. It is pretty simple, but for some techniques you don't use often there is an excellent [cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) that should be in your bookmarks.

## 1. The gist way

Gist is most commonly a single versioned document and it is perfect for event reports. All you need is GitHub account.

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

## 2. Ask for a draft

This way is a bit more advanced but allows others to be aware of your work on the report, and also allows multiple people to edit it. This method is easier than the next one and all steps can be done in the browser, at the cost of some admin work.

1. [Contact admins](#contact-admins) and ask to create a draft for you.
2. You will be invited as a collaborator to this or intermediate repository and provided a link to the draft.
3. Edit the draft as necessary.
4. When finished, [create a pull request](https://help.github.com/en/articles/creating-a-pull-request) or ask to do it for you.

## 3. Submit a pull request

This way is most advanced but is also most flexible and requires less admin assistance.

1. [Fork](https://help.github.com/en/categories/collaborating-with-issues-and-pull-requests) the events repository.
2. Create a file with your report or change an existing file in the `reports` directory. The file name must follow the format `YYYYMMDD-title-city-country.md`, e.g. `20190116-tnabc-miami-usa.md`. For content you can use [this template](https://raw.githubusercontent.com/decredcommunity/events/docs/report-template.md) as a starting point.
3. Create a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) against the events repository.
  * Check `Allow edits from maintainers` ([help](https://help.github.com/en/articles/allowing-changes-to-a-pull-request-branch-created-from-a-fork)).
  * Optionally, use [Draft pull request](https://help.github.com/en/articles/about-pull-requests#draft-pull-requests) that cannot be merged until you mark it as ready.

## Contact admins

To get your reports merged or to propose an improvement:

* either [create an issue](https://github.com/decredcommunity/events/issues)
* or ask in #event\_planning chat room via [Matrix](https://decred.org/matrix/), [Discord](https://discord.gg/GJ2GXfz) or [Slack](https://slack.decred.org/) (ping @bee)
