# Events index specification

Version: 0.4

## Event ID

Event ID is a string formatted as `YYYYMMDD.N`:

- `YYYYMMDD` is the date part of [`start_utc`](#start_utc) field

- `N` is the number of the event in that day. It is generated in order in which entries are added to the index and _not_ in order in which events occurred. The latter is desirable but not required.

## File names of index entries

Index entries must have file names formatted as `YYYYMMDD.N.yml`. That is Event ID plus `.yml` extension.

## Fields

### title

Title of the event.

When there are more than one title to choose from, these "scope rules" apply:

- The simple case is when the entire event is dedicated to Decred and there is only one title to choose from.

- For large events where Decred is just one participant, this is the title of the full event, and Decred talks must go into `subevents` field.

### title_XX

Non-English events may have a field like `title_es` or `title_pt` with the value set to title in the original language.

### lang

Comma-separated list with short codes for languages spoken at the event, e.g. `en`, `es`, `pt`, `ar`, `zh`.

Example:

    lang: en

    lang: ar, en, fr

### start_utc

Start date and time of the event. UTC time.

Same scope rules as for `title`.

- `2020-08-01`
- `2020-08-01 14:00`

### end_utc

End date and time of the event. UTC time.

Same scope rules as for `title`.

### announcements

List of links (Twitter, Eventbrite, MeetUp, Facebook, Matrix, anything).

Announcements must have been published _before_ the event, otherwise the links belong to `media`.

### location

`location` field encodes one or more places where the event took place, physical or virtual.

Formats:

- `location`
- `location1; location2; ...`

Format for events in the physical world:

    country / city / optional address

Format for events in the Internet:

    Internet / Platform1, Platform2, ...

Examples:

    Mexico / Mexico City / Awesome Hotel

    Internet / Zoom

    Internet / Skype

    Internet / YouTube, Facebook, Periscope

    Morocco / Casablanca ; Internet / Zoom

### organizers

Key facts about each co-organizer. Optionally, add individuals.

Example:

    - org: Decred
      url: https://decred.org
      person: elian
    - org: Bitcoin Embassy Jupiter
      person: Sam
      url: https://twitter.com/bitcoinembjupiter

### subevents

Smaller events that happened as part of the main event.

Most fields in each subevent follow the same rules as fields for the "outer" main event. The only exception is that subevents have a comma-separated flat list of people in the `presenters` field, as opposed to a real YAML list in `decred_people` field.

Examples:

    subevents:
      - title: Decred contractor model
        title_es: Optional non-English title here
        start_utc: 2020-08-02 14:00
        end_utc: 2020-08-02 14:30
        announcements:
          - http://url1
          - http://url2
        presenters: elian, not_elian
        description: Single-line or multi-line description of this subevent.
        attendance:
          - 100 people registered for the webinar
          - 50 people made it to the end
        media:
          - http://media1
          - url: http://complex-media2
            title: Complex Media 2
            note: so complex
        notes:
          - note1
          - note2

### decred_people

Decred community members who attended the event.

Example:

    decred_people:
      - elian
      - adcade

### attendance

List of items describing various stats about attendance.

Simple list for now, will add more formal structure as it becomes clear what data is important to capture.

Example:

    attendance:
      - 1500 people signed up for the main event
      - 1000 people attended the main event
      - 80 people attended Decred talk
      - 60 people made it till the end of Decred talk
      - 100 YouTube views as of streaming

### description

Description of the event or Decred presence part(s). Multi-line text allowed.

Example:

    description: It was a good event.

Example with multi-line text:

    description: |
      It was a good event.

      Really good event.

### media

Any media published as a product of the event (Twitter, YouTube, news coverage, etc)

Either simple list of URLs

    - https://www.youtube.com/watch?v=z-6a_tgE89E
    - https://www.youtube.com/watch?v=z-6a_tgE89E

Or `url` and `title` pairs:

    - url: https://www.youtube.com/watch?v=z-6a_tgE89E
      title: Decred contractor model
    - url: https://www.youtube.com/watch?v=z-6a_tgE89E
      title: Decred kitchen sink

### notes

List of arbitrary notes. Put any notable facts here.

Example:

    notes:
      - Decred was a Silver sponsor
      - we got too many questions about dcrtime
