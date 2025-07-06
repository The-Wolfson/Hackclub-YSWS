from datetime import datetime, timezone

from ..model.event.response import Response
from ..model.event.event import Event, Modality
from enum import Enum

def event_list(context):
    query = context.req.query
    sort: Sort = Sort(query.get("sort")) if query.get("sort") else Sort.Date
    filter: Filter = Filter(query.get("filter")) if query.get("filter") else Filter.Active
    modality: Modality | None = Modality(query.get("modality")) if query.get("modality") else None

    response: Response = Response("https://dash.hackathons.hackclub.com/api/v1/hackathons")

    events: list[Event] = sort_events(modality_filter(filter_events(response.events, filter), modality), sort)

    context.log(f"Event List — Sort: {sort}, Modality: {modality}, Filter: {filter}")

    return context.res.json(
        {
            "blocks": [block for event in events[:10] for block in event.to_blocks()]
        }
    )

class Filter(Enum):
    All = "all" # default
    Active = "active"
    Ended = "ended"
    Upcoming = "upcoming"

class Sort(Enum):
    Modality = "modality"
    Alphabetical = "alphabetical"
    Date = "date"  # default

def sort_events(events: list[Event], sort: Sort) -> list[Event]:
    match sort:
        case Sort.Modality:
            return sorted(events, key=lambda event: event.modality.value)
        case Sort.Alphabetical:
            return sorted(events, key=lambda event: event.name)
        case _:  # Date
            return sorted(events, key=lambda event: event.starts_at, reverse=True)

def filter_events(events: list[Event], filter: Filter) -> list[Event]:
    match filter:
        case Filter.All:
            return events
        case Filter.Ended:
            return [event for event in events if event.ends_at < datetime.now(timezone.utc)]
        case Filter.Upcoming:
            return [event for event in events if event.starts_at > datetime.now(timezone.utc)]
        case _:  # Active
            return [event for event in events if event.starts_at <= datetime.now(timezone.utc) and (not event.ends_at >= datetime.now(timezone.utc))]

def modality_filter(events: list[Event], modality: Modality | None) -> list[Event]:
    match modality:
        case Modality.ONLINE:
            return [event for event in events if event.modality == Modality.ONLINE]
        case Modality.IN_PERSON:
            return [event for event in events if event.modality == Modality.IN_PERSON]
        case Modality.HYBRID:
            return [event for event in events if event.modality == Modality.HYBRID]
        case _:
            return events

