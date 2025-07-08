import re
import urllib.parse
from datetime import datetime, timezone
from ..model.event.response import Response
from ..model.event.event import Event
from enum import Enum


def event_list(context):
    body: str = context.req.body
    query = context.req.query

    # Decode the body to extract the 'text' parameter
    parsed = urllib.parse.parse_qs(body)
    text = parsed.get("text", [""])[0]  # default to "" if 'text' not found

    # Extract --filter: and --sort: values from text
    filter_match = re.search(r'--filter:([^\s]+)', text)
    sort_match = re.search(r'--sort:([^\s]+)', text)
    type_match = re.search(r'--modality:([^\s]+)', text)

    # Determine Sort and Filter values
    sort: Sort = (
        Sort(sort_match.group(1))
        if sort_match and sort_match.group(1) in Sort.__members__.values()
        else Sort(query.get("sort"))
        if query.get("sort") and query.get("sort") in Sort.__members__.values()
        else Sort.Date
    )

    filter: Filter = (
        Filter(filter_match.group(1))
        if filter_match and filter_match.group(1) in Filter.__members__.values()
        else Filter(query.get("filter"))
        if query.get("filter") and query.get("filter") in Filter.__members__.values()
        else Filter.Upcoming
    )

    type: Type = (
        Type(type_match.group(1))
        if type_match and type_match.group(1) in Type.__members__.values()
        else Type(query.get("type"))
        if query.get("type") and query.get("type") in Type.__members__.values()
        else Type.All
    )

    response: Response = Response("https://events.hackclub.com/api/events/all/")

    events: list[Event] = sort_events(type_filter(filter_events(response.events, filter), type), sort)

    context.log(f"Event List — Sort: {sort}, Modality: {type}, Filter: {filter}")

    return context.res.json(
        {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Hackclub Events"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Filter"
                            },
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": filter.name
                                },
                                "value": filter.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": f.name
                                    },
                                    "value": f.value
                                } for f in Filter
                            ]
                        },
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Sort"
                            },
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": sort.name
                                },
                                "value": sort.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": s.name
                                    },
                                    "value": s.value
                                } for s in Sort
                            ]
                        },
                        {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Modality"
                            },
                            "initial_option": {
                                "text": {
                                    "type": "plain_text",
                                    "text": type.name
                                },
                                "value": type.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": t.name
                                    },
                                    "value": t.value
                                } for t in Type
                            ]
                        }
                    ]
                },
                *[block for event in events[:10] for block in event.to_blocks()]
            ]
        }
    )


class Filter(Enum):
    All = "all"
    Ended = "ended"
    Upcoming = "upcoming"  # default


class Type(Enum):
    All = "all"  # default
    Event = "event"
    Ama = "ama"


class Sort(Enum):
    Alphabetical = "alphabetical"
    Date = "date"  # default


def sort_events(events: list[Event], sort: Sort) -> list[Event]:
    match sort:
        case Sort.Alphabetical:
            return sorted(events, key=lambda event: event.name)
        case _:  # Date
            return sorted(events, key=lambda event: event.start, reverse=True)


def filter_events(events: list[Event], filter: Filter) -> list[Event]:
    match filter:
        case Filter.All:
            return events
        case Filter.Ended:
            return [event for event in events if event.end < datetime.now(timezone.utc)]
        case Filter.Upcoming:
            return [event for event in events if event.start > datetime.now(timezone.utc)]
        case _:  # Active
            return [event for event in events if
                    event.start <= datetime.now(timezone.utc) and (not event.end >= datetime.now(timezone.utc))]


def type_filter(events: list[Event], type: Type) -> list[Event]:
    match type:
        case Type.Event:
            return [event for event in events if event.ama == False]
        case Type.Ama:
            return [event for event in events if event.ama == True]
        case _:  # All
            return events
