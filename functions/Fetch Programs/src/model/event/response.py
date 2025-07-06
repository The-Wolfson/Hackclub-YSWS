from dataclasses import dataclass
from .event import Event

import requests

@dataclass
class Links:
    next: str

    def __init__(self, data: dict):
        self.next = data.get("next")


@dataclass
class Meta:
    total_count: int
    total_pages: int

    def __init__(self, data: dict):
        self.total_count = data.get("total_count")
        self.total_pages = data.get("total_pages")


@dataclass
class Response:
    events: list[Event]
    links: Links
    meta: Meta

    def __init__(self, url: str):
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        self.events = [Event(e) for e in data.get("data", [])]
        self.links = Links(data.get("links"))
        self.meta = Meta(data.get("meta"))
