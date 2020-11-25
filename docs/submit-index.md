# Submit your event to the index

The index of past Decred events is published here: https://decredcommunity.github.io/events/index/

You can get your event listed and receive a [nice link](https://decredcommunity.github.io/events/index/20200925.1) that contains everything about the event. You can then use this link in reporting.

Currently we use a rather complex approach where the information is captured in [YAML files](https://github.com/decredcommunity/events/tree/master/index). Saving data this way allows to generate a [website](https://decredcommunity.github.io/events/index/) automatically, at the cost of some work to write the files manually. In the future it may be simplified if somebody builds a pretty GUI to enter the data.

## Add event via the browser

- open the [index](https://github.com/decredcommunity/events/tree/master/index) directory in a new tab

- click `Add file`, then `Create new file`

- in the `Name your file...` box enter the filename in the format `YYYYMMDD.X.yml`:

  - first part is the UTC date, e.g. `20201125`
  - please check your time zone. If the event started on Nov 25 22:00 in UTC-5 time zone, the UTC time is Nov 26 03:00 and so the filename should be `20201126`.
  - second part `X` is the event number. Use lowest available number, or `1` if no events are registered for that day.
  - last part is the `.yml` extension, giving us `20201125.1.yml`

- copy the template from [here](https://raw.githubusercontent.com/decredcommunity/events/master/index/0_template.yml) into the editor

- fill the values, use [existing entry](https://github.com/decredcommunity/events/blob/master/index/20200820.1.yml) as an example

  - we use [YAML](https://en.wikipedia.org/wiki/YAML) syntax that has a good balance between human readability and capturing structured data for use in automated report generation
  - `lang` must be language short code like `en` `es` `pt` `zh`
  - `start_utc` is UTC time when the event started, e.g. `2020-11-25 22:00`
  - `end_utc` is optional
  - `announcements` is a list of links where the event was announced (Twitter, Eventbrite, MeetUp etc)
  - `location` must be `Country / City / any address detail` or `Internet / Platform1, Platform2, Platform3`
  - `organizers` captures names and homepages of organizations that helped to run the event. `person` is optional but helps to capture individual contributions. Add more blocks if more than one organization was involved.
  - `decred_people` is a list of names, most commonly Decred Matrix usernames
  - `attendance` captures any useful info about how many people registered/attended/watched/asked questions/etc
  - `description` is an arbitrary text describing the event.
  - `media` is a list of media created during or after the event, like YouTube videos, photos, news coverage, tweets, etc
  - `notes` captures anything that didn't fit in the other fields
  - remove fields you don't need, e.g. most entries are small events and don't need `decred_talks` section

- at the bottom of the page switch to `Create a new branch for this commit and start a pull request`

- click `Commit new file`

- adjust pull request title and description and click `Create pull request`
