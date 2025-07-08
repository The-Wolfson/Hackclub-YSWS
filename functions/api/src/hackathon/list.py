import re
import urllib.parse
from datetime import datetime, timezone

from ..model.hackathon.response import Response
from ..model.hackathon.hackathon import Hackathon, Modality
from enum import Enum


def hackathon_list(context):
    body: str = context.req.body
    query = context.req.query

    # Decode the body to extract the 'text' parameter
    parsed = urllib.parse.parse_qs(body)
    text = parsed.get("text", [""])[0]  # default to "" if 'text' not found

    # Extract --filter: and --sort: values from text
    filter_match = re.search(r'--filter:([^\s]+)', text)
    sort_match = re.search(r'--sort:([^\s]+)', text)
    modality_match = re.search(r'--modality:([^\s]+)', text)

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
        else Filter.Active
    )

    modality: Modality = (
        Modality(modality_match.group(1))
        if modality_match and modality_match.group(1) in Modality.__members__.values()
        else Modality(query.get("modality"))
        if query.get("modality") and query.get("modality") in Modality.__members__.values()
        else Modality.ALL
    )

    response: Response = Response("https://dash.hackathons.hackclub.com/api/v1/hackathons")

    events: list[Hackathon] = sort_hackathons(modality_filter(filter_hackathons(response.hackathons, filter), modality),
                                              sort)

    context.log(f"Event List — Sort: {sort}, Modality: {modality}, Filter: {filter}")

    return context.res.json(
        {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Hackathons"
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
                                    "text": modality.name
                                },
                                "value": modality.value
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": m.name
                                    },
                                    "value": m.value
                                } for m in Modality
                            ]
                        }
                    ]
                },
                *[block for event in events[:10] for block in event.to_blocks()]
            ]
        }
    )


class Filter(Enum):
    All = "all"  # default
    Active = "active"
    Ended = "ended"
    Upcoming = "upcoming"


class Sort(Enum):
    Modality = "modality"
    Alphabetical = "alphabetical"
    Date = "date"  # default


def sort_hackathons(hackathons: list[Hackathon], sort: Sort) -> list[Hackathon]:
    match sort:
        case Sort.Modality:
            return sorted(hackathons, key=lambda event: event.modality.value)
        case Sort.Alphabetical:
            return sorted(hackathons, key=lambda event: event.name)
        case _:  # Date
            return sorted(hackathons, key=lambda event: event.starts_at, reverse=True)


def filter_hackathons(hackathons: list[Hackathon], filter: Filter) -> list[Hackathon]:
    match filter:
        case Filter.All:
            return hackathons
        case Filter.Ended:
            return [event for event in hackathons if event.ends_at < datetime.now(timezone.utc)]
        case Filter.Upcoming:
            return [event for event in hackathons if event.starts_at > datetime.now(timezone.utc)]
        case _:  # Active
            return [event for event in hackathons if
                    event.starts_at <= datetime.now(timezone.utc) and (not event.ends_at >= datetime.now(timezone.utc))]


def modality_filter(events: list[Hackathon], modality: Modality) -> list[Hackathon]:
    match modality:
        case Modality.ONLINE:
            return [event for event in events if event.modality == Modality.ONLINE]
        case Modality.IN_PERSON:
            return [event for event in events if event.modality == Modality.IN_PERSON]
        case Modality.HYBRID:
            return [event for event in events if event.modality == Modality.HYBRID]
        case _:
            return events
